"""This module contains the model used for the homepage."""
from django.db import models

from mezzanine.core.models import SiteRelated
from mezzanine.core.fields import RichTextField


class HomepageContent(SiteRelated):
    """A singelton model for holding the content of the Home Page.

    .. attribute:: intro_text

        The larger text directly below the navigation

    .. attribute:: content_title

        The title for the section of custom content

    .. attribute:: content

        The content of the custom section of the home page

    .. attribute:: show_news

        Whether or not to display the ``News`` block

    .. attribute:: show_newest_communities

        Whether or not to display the ``Newest Communities`` block

    """
    intro_text = RichTextField(
        help_text="The large text below the navigation",
    )
    content_title = models.CharField(
        max_length=200,
        default="Our Principles",
        help_text="The title of the custom content section",
    )
    content = RichTextField(
        help_text="The custom text",
    )
    show_news = models.BooleanField(
        default=True,
        help_text='Display the "News" block?',
    )
    show_newest_communities = models.BooleanField(
        default=True,
        help_text='Display the "Newest Communities" block?',
    )

    class Meta(object):
        """Correct the Display Name."""
        verbose_name = 'Homepage Content'
        verbose_name_plural = 'Homepage Content'

    def only_show_content(self):
        """Determine if we show only the content."""
        return not (self.show_news or self.show_newest_communities)
