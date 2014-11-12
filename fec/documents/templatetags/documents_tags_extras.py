"""This module includes templatetags that rely on `documents_tags`."""
from django import template


register = template.Library()


@register.inclusion_tag('documents/tags/documents_and_subcategories.html')
def categorys_docs_and_cats(category):
    """Render a Category's Documents and it's Child Categories.

    :param category: The Document Category to use.
    :type category: :class:`..models.DocumentCategory`

    """
    return {'category': category}
