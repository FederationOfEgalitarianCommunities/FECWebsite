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
    """Return a random Published Community that has a full_description."""
    communities = Community.objects.published().exclude(
        full_description__exact='').order_by('?')
    return communities[0] if communities else None


@register.assignment_tag
def community_all_latest_posts(limit=10):
    """Return the latest RSS Feed & Blog Posts of all the Communities.

    Posts with duplicate titles are removed, preferring Posts from Member
    Communities.

    """
    communities = (
        list(Community.objects.filter(
            membership_status=Community.MEMBER).order_by('?')) +
        list(Community.objects.exclude(membership_status=Community.MEMBER)))
    feed_posts = []
    post_titles = []
    for community in communities:
        for post in community.get_latest_posts():
            if post['title'] not in post_titles:
                post_titles.append(post['title'])
                feed_posts.append(post)
    posts = sorted(feed_posts, key=lambda post: post['published'],
                   reverse=True)
    return posts[:limit]


@register.assignment_tag
def community_fec_members():
    """Return a list of all FEC member communities."""
    return Community.objects.published().filter(
        membership_status=Community.MEMBER)


@register.assignment_tag
def community_communities_in_dialog():
    """Return a list of all FEC Communities in dialog"""
    return Community.objects.published().filter(
        membership_status=Community.COMMUNITY_IN_DIALOG)


@register.assignment_tag
def community_newest_communities(limit=5):
    """Return a list of FEC Communities ordered by creation date."""
    return Community.objects.published().exclude(
        membership_status=Community.ALLY).order_by('-date_joined')[:limit]
