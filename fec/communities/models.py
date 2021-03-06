"""This module contains data models related to Communities."""
from datetime import datetime
import re
from string import punctuation
from time import mktime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import force_text
import feedparser
from mezzanine.blog.models import BlogCategory
from mezzanine.core.models import (Displayable, Orderable,
                                   CONTENT_STATUS_PUBLISHED)
from mezzanine.core.fields import RichTextField, FileField
from mezzanine.utils.models import upload_to


class Community(Displayable):
    """A model for FEC Communities.

    .. attribute:: MEMBER

        A constant representing an FEC Full Member Community.

    .. attribute:: COMMUNITY_IN_DIALOG

        A constant representing an FEC Full Community in Dialog.

    .. attribute:: ALLY

        A constant representing an Ally Community of the FEC.

    .. attribute:: STATUS_CHOICES

        The available choices for the ``membership_status`` field.

    .. attribute:: profile_image

        The main image to use for the Community.

    .. attribute:: short_description

        A short paragraph about the community.

    .. attribute:: full_description

        An in-depth description about the community.

    .. attribute:: general_location

        The general area of the Community(e.g., "Rural Virginia").

    .. attribute:: year_founded

        The year the Community was initially founded.

    .. attribute:: number_of_adults

        The number of adults living in the Community.

    .. attribute:: number_of_children

        The number of children living in the Community.

    .. attribute:: membership_status

        The current FEC membership status of the Community. Can be Member,
        Community in Dialog or Ally.

    .. attribute:: date_joined

        The day the Community became a Community in Dialog. Blank for
        non-members. Used primarily to sort the Newest Communities widget on
        the homepage.

    .. attribute:: address

        The Community's full address.

    .. attribute:: website

        The Community's website.

    .. attribute:: email

        The contact email of the Community.

    .. attribute:: phone

        The phone number of the Community.

    .. attribute:: blog_category

        The :class:`mezzanine.blog.models.BlogCategory` containing the
        Community's posts.

    """
    MEMBER = 'member'
    COMMUNITY_IN_DIALOG = 'community-in-dialog'
    ALLY = 'ally'
    STATUS_CHOICES = (
        (MEMBER, 'Full Member'),
        (COMMUNITY_IN_DIALOG, 'Community in Dialog'),
        (ALLY, 'Ally')
    )

    profile_image = models.ImageField(
        blank=True, null=True,
        upload_to='communities/profile_images/',
        help_text='The main image to use for the Community.'
    )
    short_description = models.TextField(
        blank=True,
        help_text='A short paragraph about the community. This is used on the '
        'Our Communities page.'
    )
    full_description = RichTextField(
        blank=True,
        help_text='A long description about the community. This is used on '
        'the Community\'s detail page.'
    )
    general_location = models.CharField(
        blank=True,
        help_text='The general area of the Community, like "Rural Virginia".',
        max_length=50
    )
    year_founded = models.PositiveSmallIntegerField(
        blank=True, null=True,
        help_text='The year the community was founded.'
    )
    number_of_adults = models.PositiveSmallIntegerField(
        default=0,
        help_text='The number of adults living in the Community.'
    )
    number_of_children = models.PositiveSmallIntegerField(
        default=0,
        help_text='The number of children living in the Community.'
    )
    membership_status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=30,
        default=COMMUNITY_IN_DIALOG,
        verbose_name='FEC Membership Status',
        help_text='The Community\'s current status with the FEC.'
    )
    date_joined = models.DateField(
        blank=True, null=True,
        help_text=('The date this Community became a Community in Dialog. '
                   'You can leave this blank if it\'s an Ally. '
                   'This field is used to sort the Newest Communities widget '
                   'on the homepage.'),
        verbose_name='In FEC Since'
    )
    address = models.TextField(
        blank=True,
        help_text='The full address of the Community.',
        verbose_name='Full Address'
    )
    website = models.URLField(
        blank=True,
        help_text='The Community\'s website.'
    )
    email = models.EmailField(
        blank=True,
        help_text='The contact email for the Community.',
        verbose_name='Contact Email'
    )
    phone = models.CharField(
        blank=True,
        help_text='The phone number of the Community.',
        verbose_name='Phone Number',
        max_length=20
    )
    blog_category = models.ForeignKey(
        BlogCategory,
        blank=True,
    )

    class Meta(object):
        """Set the model's options, like the plural name and ordering."""
        verbose_name_plural = 'communities'
        ordering = ['title']

    def __unicode__(self):
        """Use the :attr:`Community.title <name>` to represent it."""
        return u'{}'.format(self.title)

    def get_absolute_url(self):
        """Return the URL of the Community's Detail Page."""
        if self.membership_status == Community.COMMUNITY_IN_DIALOG:
            return reverse('community_in_dialog_detail',
                           kwargs={'slug': self.slug})
        elif self.membership_status == Community.ALLY:
            return reverse('ally_community_detail', kwargs={'slug': self.slug})
        return reverse('community_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """Create the :attr:`blog_category` or update it's name."""
        if not self.id:
            self.blog_category = BlogCategory.objects.create(title=self.title)
        else:
            self.blog_category.title = self.title
            self.blog_category.save()
        super(Community, self).save(*args, **kwargs)

    def get_latest_posts(self, limit=5):
        """
        Return a list of latest BlogPosts in Community's BlogCategory and Posts
        from it's CommunityFeed.

        """
        blog_and_feed_posts = (
            [convert_to_feed_post(blog_post, self) for blog_post in
             self.blog_category.blogposts.filter(
                 status=CONTENT_STATUS_PUBLISHED)] +
            self.get_latest_feed_posts()
        )
        blog_and_feed_posts.sort(
            key=lambda post: post['published'], reverse=True)

        return blog_and_feed_posts[:limit]

    def get_latest_feed_posts(self):
        """Return a list of the Community's latest ``feed posts``.

        What exactly consitutes a ``feed_post`` is defined by the
        :func:`CommunityFeed.get_feed_posts` function.

        A `community` attribute is added to each post containing the parent
        :class:`Community`.

        :returns: A list of ``feed post`` dictionaries.

        """
        feeds = self.feeds.all()
        feed_posts = []
        _ = [feed_posts.append(post) for feed in feeds
             for post in feed.get_feed_posts()]
        _ = [setattr(post, "community", self) for post in feed_posts]
        feed_posts.sort(key=lambda x: x.published, reverse=True)
        return feed_posts[:5]


class CommunityImage(Orderable, object):
    """A model for :class:`Community` gallery images.

    This has been ripped and repurposed from
    :class:`mezzanine.galleries.models.GalleryImage`.

    """
    community = models.ForeignKey(Community, related_name="images")
    file = FileField(
        "File",
        max_length=200,
        format="Image",
        upload_to=upload_to("communities.CommunityImage.file",
                            "community-galleries")
    )
    description = models.CharField("Description", max_length=1000, blank=True)

    class Meta(object):
        """Set the colloquial name to ``Image``."""
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id and not self.description and hasattr(self.file, 'name'):
            name = force_text(self.file.name)
            name = name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(CommunityImage, self).save(*args, **kwargs)


class CommunityFeed(Orderable, object):
    """A model for :class:`Community` RSS and Atom feeds.

    .. attribute:: url

        The URL of the RSS Feed

    .. attribute:: community

        The :class:`Community` the feed belongs to.

    .. attribute:: post_limit

        The maximum number of posts to display.

    """
    url = models.URLField(help_text='The Feed\'s URL.')
    community = models.ForeignKey(Community, related_name="feeds")
    post_limit = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta(object):
        """Set the colloquial name to ``Feed``."""
        verbose_name = "Feed"
        verbose_name_plural = "Feeds"

    def __unicode__(self):
        return self.url

    def get_feed_posts(self):
        """Return all feed posts from the :attr:`url`.

        This modifies the ``published`` attribute to be a datetime instead of
        the Feed's date string.

        :returns: A list of ``feed posts``.
        """
        parsed_feed = feedparser.parse(self.url)
        posts = parsed_feed.entries
        for post in posts:
            published_datetime = datetime.fromtimestamp(mktime(
                post['published_parsed']))
            post['published'] = published_datetime
            post['via'] = re.sub(r'^(http(s)?://)?(www.)?(.*)$', r'\4',
                                 parsed_feed.feed.link)
        if self.post_limit is not None:
            return posts[:self.post_limit]
        return posts


def convert_to_feed_post(blog_post, community):
    '''Turn a BlogPost into a feedparser entry.'''
    return {
        'title': blog_post.title,
        'published': blog_post.publish_date.replace(tzinfo=None),
        'author': blog_post.user.get_full_name(),
        'description': blog_post.description,
        'link': blog_post.get_absolute_url(),
        'comments': '{}#comments'.format(blog_post.get_absolute_url()),
        'slash_comments': '{}'.format(blog_post.comments_count),
        'community': community,
    }
