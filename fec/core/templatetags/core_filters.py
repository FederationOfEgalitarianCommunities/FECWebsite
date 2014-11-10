"""This module defines general template filters."""
from django import template


register = template.Library()


@register.filter(name="get_first_by")
def get_first_by(value, stop_char):
    """Split the string by the ``stop_char`` and return the first item.

    :param value: The value passed to the filter.
    :type value: string
    :param stop_char: The character the split the ``value`` by.
    :type stop_char: string
    :returns: The resultant sub-string.

    """
    return unicode(value).split(stop_char)[0]
