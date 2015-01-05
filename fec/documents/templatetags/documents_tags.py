"""This module contains template includes associated with Documents."""
from django import template
from django.db.models import Count

from ..models import Document, DocumentCategory


register = template.Library()


@register.inclusion_tag('documents/tags/document_list_group.html')
def document_list_group(documents, show_tags=True):
    """Render the Category's Documents as a Bootstrap list group.

    :param documents: The Documents to be shown.
    :type documents: A list of :class:`..models.Document`

    """
    return {'documents': documents, 'show_tags': show_tags}


@register.inclusion_tag('documents/tags/category_breadcrumbs.html')
def category_breadcrumbs(category, is_active=False):
    """Render a Category and it's parent a breadcrumb.

    :param category: The Document Category to display.
    :type category: :class:`..models.DocumentCategory`
    :param is_active: If the category is the active breadcrumb.
    :type is_active: Boolean

    """
    return {'category': category, 'is_active': is_active}


@register.assignment_tag
def documents_newest():
    """Return the 5 newest Documents."""
    return Document.objects.all().order_by('-created')[:3]


@register.assignment_tag
def categories_top():
    """Return the 5 DocumentCategories with the highest number of documents."""
    return DocumentCategory.objects.annotate(
        document_count=Count('document')).order_by('-document_count')[:5]
