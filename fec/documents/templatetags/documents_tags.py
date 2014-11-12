"""This module contains template includes associated with Documents."""
from django import template


register = template.Library()


@register.inclusion_tag('documents/tags/document_list_group.html')
def document_list_group(documents):
    """Render the Category's Documents as a Bootstrap list group.

    :param documents: The Documents to be shown.
    :type documents: A list of :class:`..models.Document`

    """
    return {'documents': documents}


@register.inclusion_tag('documents/tags/category_breadcrumbs.html')
def category_breadcrumbs(category, is_active=False):
    """Render a Category and it's parent a breadcrumb.

    :param category: The Document Category to display.
    :type category: :class:`..models.DocumentCategory`
    :param is_active: If the category is the active breadcrumb.
    :type is_active: Boolean

    """
    return {'category': category, 'is_active': is_active}
