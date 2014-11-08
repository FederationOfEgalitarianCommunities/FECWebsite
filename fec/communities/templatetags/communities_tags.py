"""This module contains templatetags associated with Communities."""
from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag('communities/tags/thumbnail_block_info.html')
def community_info_thumbnail_block(community):
    """Render information about the community in a thumbnail and caption.

    Includes the :attr:`~..models.Community.title`,
    :attr:`~..models.Community.year_founded`, ``population``,
    :attr:`~..models.Community.general_location` and
    :attr:`~..models.Community.short_description`.

    :param community: The Community whose profile picture should be shown.
    :type community: :class:`..models.Community`

    """
    return {'community': community,
            'MEDIA_URL': settings.MEDIA_URL}


@register.inclusion_tag('communities/tags/description_list_info.html')
def community_info_description_list(community):
    """Render information about the community using a description list.

    Includes the :attr:`~..models.Community.year_founded`, ``population``,
    :attr:`~..models.Community.address`
    :attr:`~..models.Community.website`, :attr:`~..models.Community.email`,
    and :attr:`~..models.Community.phone`.

    :param community: The Community whose profile picture should be shown.
    :type community: :class:`..models.Community`

    """
    return {'community': community}


@register.inclusion_tag('communities/tags/profile_picture.html')
def community_profile_picture_thumbnail(community, width, height):
    """Render a thumnbail of a :attr:`~..models.Community.profile_image`.

    :param community: The Community whose profile picture should be shown.
    :type community: :class:`..models.Community`
    :param width: The width of the thumbnail.
    :type width: :class:`Integer`
    :param height: The height of the thumbnail.
    :type height: :class:`Integer`

    """
    return {'community': community,
            'width': width,
            'height': height,
            'MEDIA_URL': settings.MEDIA_URL}