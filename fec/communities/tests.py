"""This module contains unit tests for the ``communities`` package."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Community, CommunityFeed


class CommunityModelTests(TestCase):
    """Test the Community Model Methods."""
    def setUp(self):
        """Create a Community and RSS Feed."""
        self.community = Community.objects.create(title="Dreamland")
        CommunityFeed.objects.create(
            community=self.community,
            url="http://www.feedforall.com/sample-feed.xml")

    def test_get_latest_blog_posts_returns_latest_posts(self):
        """get_latest_blog_posts should return the 5 latest posts."""
        bps = self.community.get_latest_blog_posts()
        post_titles = [
            'Recommended Web Based Feed Reader Software',
            'Recommended Desktop Feed Reader Software',
            'RSS Resources',
        ]
        self.assertSequenceEqual([post.title for post in bps], post_titles)


class CommunityFeedModelTests(TestCase):
    """Test the CommunityFeed Model Methods."""
    def setUp(self):
        """Create a Community and RSS Feed."""
        self.community = Community.objects.create(
            membership_status=Community.MEMBER, title="Dreamland")
        self.feed = CommunityFeed.objects.create(
            community=self.community,
            url="http://www.feedforall.com/sample-feed.xml")

    def test_get_blog_posts_returns_feeds_posts(self):
        """get_blog_posts should return all posts from the CommunityFeed."""
        bps = self.feed.get_blog_posts()
        post_titles = [
            'RSS Resources',
            'Recommended Desktop Feed Reader Software',
            'Recommended Web Based Feed Reader Software',
        ]
        self.assertEqual([post.title for post in bps], post_titles)

    def test_get_blog_posts_respects_post_limit(self):
        """get_latest_blog_posts should limit the items to the post_limit."""
        self.feed.post_limit = 1
        self.feed.save()
        bps = self.feed.get_blog_posts()
        post_titles = ['RSS Resources']
        self.assertSequenceEqual([post.title for post in bps], post_titles)


class CommunityDetailViewTests(TestCase):
    """Test the DetailViews Associated with the Community Model."""
    def setUp(self):
        """Create a Community to view."""
        self.community = Community.objects.create(
            membership_status=Community.MEMBER, title="Dreamland")
        self.community_in_dialog = Community.objects.create(
            title="Dreamland 2",
            membership_status=Community.COMMUNITY_IN_DIALOG)
        self.ally = Community.objects.create(
            title="Dreamland 3", membership_status=Community.ALLY)

    def test_community_detail_redirects_others(self):
        """
        The CommunityDetail view should redirect to the proper view if the
        community is not a member of the FEC.
        """
        response = self.client.get(
            reverse('community_detail',
                    kwargs={'slug': self.community_in_dialog.slug}))
        self.assertRedirects(response,
                             self.community_in_dialog.get_absolute_url())

        response = self.client.get(
            reverse('community_detail', kwargs={'slug': self.ally.slug}))
        self.assertRedirects(response, self.ally.get_absolute_url())

    def test_community_in_dialog_detail_redirects_others(self):
        """
        The CommunityInDialogDetail view should redirect to the proper view if
        the community is not a community in dialog.
        """
        response = self.client.get(
            reverse('community_in_dialog_detail',
                    kwargs={'slug': self.community.slug}))
        self.assertRedirects(response, self.community.get_absolute_url())

        response = self.client.get(
            reverse('community_in_dialog_detail',
                    kwargs={'slug': self.ally.slug}))
        self.assertRedirects(response, self.ally.get_absolute_url())

    def test_ally_detail_redirects_others(self):
        """
        The AllyCommunityDetail view should redirect to the proper view if the
        community is not an ally community..
        """
        response = self.client.get(
            reverse('ally_community_detail',
                    kwargs={'slug': self.community.slug}))
        self.assertRedirects(response, self.community.get_absolute_url())

        response = self.client.get(
            reverse('ally_community_detail',
                    kwargs={'slug': self.community_in_dialog.slug}))
        self.assertRedirects(
            response, self.community_in_dialog.get_absolute_url())


class CommunityListViewTests(TestCase):
    """Test the ListViews Associated with the Community Model."""
    def setUp(self):
        """Create some Communities and a Community in Dialog."""
        self.darmok = Community.objects.create(
            membership_status=Community.MEMBER, title="Darmok")
        self.jalad = Community.objects.create(
            membership_status=Community.MEMBER, title="Jalad")
        self.community_in_dialog = Community.objects.create(
            title="Tenagra", membership_status=Community.COMMUNITY_IN_DIALOG)
        self.ally_community = Community.objects.create(
            title="On the Ocean", membership_status=Community.ALLY)

    def test_community_list_passes_correct_context(self):
        """The CommunityList view should pass the correct context."""
        response = self.client.get(reverse('community_list'))
        self.assertSequenceEqual([self.darmok, self.jalad],
                                 response.context['community_list'])
        self.assertSequenceEqual([self.community_in_dialog],
                                 response.context['in_dialog_list'])
        self.assertSequenceEqual([self.ally_community],
                                 response.context['ally_list'])
