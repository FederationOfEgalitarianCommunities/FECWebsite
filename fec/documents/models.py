"""This module contains data models related to Documents."""
import random

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Displayable, Slugged, Orderable
from mezzanine.utils.urls import admin_url

from communities.models import Community


class Document(Displayable):
    """A model for archiving and sharing a Community's Documents.

    .. attribute:: category

        The :class:`DocumentCategory` this Document belongs to.

    .. attribute:: community

        The (optional) :class:`~communities.models.Community` that the Document
        belongs to.

    .. attribute:: contents

        The content of the Document.

    """
    contents = RichTextField(
        help_text='The Document\'s Contents.'
    )
    community = models.ForeignKey(
        Community,
        blank=True,
        null=True,
        related_name='documents',
        related_query_name='document',
        help_text="The Community the Document belongs to."
    )
    category = models.ForeignKey(
        'DocumentCategory',
        related_name='documents',
        related_query_name='document',
        help_text="The Category to put the Document under."
    )

    class Meta(object):
        """Order by Category, then Community, then Title."""
        ordering = ('category', 'community', 'title')
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """Return the detail page of the Document."""
        return reverse('document_detail', kwargs={'slug': self.slug})

    def related_documents(self):
        """Return 5 random Documents with the same category or tag."""
        keywords = self.keywords.all()
        documents = set(
            Document.objects.filter((Q(keywords__keyword__in=keywords) |
                                     Q(category=self.category)) &
                                    (~Q(id=self.id)))
        )
        sample_size = 5 if len(documents) > 5 else len(documents)
        return random.sample(documents, sample_size)


class DocumentCategory(Orderable, Slugged):
    """A model for organizing :class:`Documents <Document>`.

    .. attribute:: parent

        The optional parent :class:`DocumentCategory`.

    """
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        related_name='children',
        related_query_name='child',
        limit_choices_to={'parent': None},
        help_text='The parent category, if any. Only one level of nesting is '
        'allowed.'
    )

    class Meta(object):
        """Set the colloquial name to ``Category``."""
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """Return the detail page of the Category."""
        return reverse('document_category_detail', kwargs={'slug': self.slug})

    def get_admin_url(self):
        """Return the Category's Edit page."""
        return admin_url(self, "change", self.id)
