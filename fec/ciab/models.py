from django.db import models
from django.utils.text import slugify

from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Orderable
from wiki.models.article import Article, ArticleRevision
from wiki.models.urlpath import URLPath


class Decision(Orderable):
    """
    A model for Commune in a Box Decisions.

    Used in the Commune-in-a-Box Choose-Your-Own-Adventure & also to generate
    Wiki pages.

    .. attribute:: name

        The name of the decision.

    .. attribute:: short_description

        A short description of the decision, shown on the CiaB page and the
        Wiki page.

    .. attribute:: long_description

        A long description of the decision, shown only on the Wiki page.

    """

    name = models.CharField(
        max_length=50,
        help_text="The display name of the Decision."
    )
    short_description = RichTextField(
        help_text="A short introduction description shown on both pages."
    )
    long_description = RichTextField(
        help_text="A long description shown on CiaB and Wiki pages."
    )
    wiki_article = models.ForeignKey(Article, blank=True)

    def __unicode__(self):
        """A Decision is labelled by it's name."""
        return self.name

    def save(self, *args, **kwargs):
        """Create a Wiki Article or Update an Existing One."""
        should_create_article = not self.id
        if should_create_article:
            self.create_article()
        super(Decision, self).save(*args, **kwargs)
        if not should_create_article:
            self.update_article()

    def create_article(self):
        """Create a new Wiki Article for this Decision."""
        parent = URLPath.root()
        url_path = URLPath.create_article(
            parent=parent,
            slug=slugify(self.name),
            title=self.name,
            article_kwargs={'group_write': False, 'other_write': False},
            user_message='Initial Creation by Commune in a Box Decision.',
            locked=True,
            content=self.to_markdown(),
        )
        self.wiki_article = url_path.article

    def update_article(self, user_message=None):
        """Update the Wiki Article for this Decision."""
        if user_message is None:
            user_message = "Automatic update by Commune in a Box Decision."
        new_revision = ArticleRevision.objects.create(
            article=self.wiki_article, title=self.name,
            content=self.to_markdown(), locked=True,
            user_message=user_message,
        )
        self.wiki_article.add_revision(new_revision)

    def to_markdown(self):
        """Return a Markdown Representation of the Decision & Options."""
        option_outputs = [option.to_markdown()
                          for option in self.option_set.all()]
        output = [
            self.short_description,
            "[TOC]",
            self.long_description,
        ] + option_outputs
        return '\n\n'.join(output)


class Option(Orderable):
    """Represents a possible choice for a Commune-in-a-Box Decision.

    .. attribute:: name

        The name of the option..

    .. attribute:: short_description

        A short description of the option, shown on the CiaB page and the
        Wiki page.

    .. attribute:: long_description

        A long description of the option, shown only on the Wiki page.

    .. attribute:: decision

        The Decision this option belongs to.

    """

    name = models.CharField(
        max_length=50,
        help_text="The display name of the Option."
    )
    short_description = RichTextField(
        help_text="A short introduction description shown on both pages."
    )
    long_description = RichTextField(
        help_text="A long description shown on CiaB and Wiki pages."
    )
    decision = models.ForeignKey(Decision)

    def __unicode__(self):
        """An Option is labelled by it's name."""
        return self.name

    def save(self, *args, **kwargs):
        """Update the Decision's Wiki Article after Saving the Option."""
        super(Option, self).save(*args, **kwargs)
        message = "Automatic Update by Commune in a Box Option - {}.".format(
            self.name)
        self.decision.update_article(user_message=message)

    def to_markdown(self):
        """Return a Markdown Representation of the Option."""
        output = [
            "## {}".format(self.name),
            self.short_description,
            self.long_description,
        ]
        return '\n\n'.join(output)
