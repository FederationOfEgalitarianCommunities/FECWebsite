"""This module contains templatetags associated with Communities."""
from django import template
from django.conf import settings

from communities.models import Community, CommunityImage


register = template.Library()


@register.inclusion_tag('communities/tags/population_and_location_text.html')
def community_population_and_location(community):
    """Render information about the community's population and location.

    :param community: The Community to use
    :type community: :class:`..models.Community`

    """
    return {'community': community}


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


@register.inclusion_tag('communities/tags/community_blurb.html')
def community_blurb(community, truncate_description_at=35, show_picture=True):
    """Render a compact blurb for a :class:`~.models.Community`.

    This includes the picture, name, population, general location, and the full
    description(truncated at the specified amount of words).
    """
    return {'community': community,
            'show_profile_picture': show_picture,
            'truncate_at': truncate_description_at}


@register.assignment_tag
def community_random_image():
    """Return a random Communityimage."""
    images = CommunityImage.objects.order_by('?')
    return images[0] if images else None


@register.assignment_tag
def community_random():
    """Return a random Community."""
    communities = Community.objects.order_by('?')
    return communities[0] if communities else None


@register.assignment_tag
def community_all_latest_blog_posts(limit=5):
    """Return the latest Blog Posts of all the Communities."""
    communities = Community.objects.all()
    posts = []
    _ = [posts.extend(community.get_latest_blog_posts()) for community in
         communities]
    posts.sort(key=lambda post: post.published, reverse=True)
    return posts


@register.assignment_tag
def community_fec_members():
    """Return a list of all FEC member communities."""
    return Community.objects.filter(is_community_in_dialog=False)


@register.assignment_tag
def community_communities_in_dialog():
    """Return a list of all FEC Communities in dialog"""
    return Community.objects.filter(is_community_in_dialog=True)
