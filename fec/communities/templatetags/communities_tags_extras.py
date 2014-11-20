"""This module contains templatetags associated with Communities.

This module is split out from the communities_tags module because these tags
depend on tags defined in communities_tags.

"""
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
