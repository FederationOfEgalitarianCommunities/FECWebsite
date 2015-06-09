"""This module contains functional tests for the Home Page."""
import datetime
from django.contrib.auth import get_user_model
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.blog.models import BlogPost

from communities.models import Community
from core.utils import SeleniumTestCase
from homepage.models import HomepageContent


class HomePageTests(SeleniumTestCase):
    """Test Expectations for the Home Page."""
    def setUp(self):
        """Create a User, the Homepage Content & visit the home page."""
        user = get_user_model()
        self.user = user.objects.create_superuser(
            'test', 'test@test.com', 'test')
        self.content = HomepageContent.objects.create(
            intro_text='The intro text should be large',
            content_title='Unboxed sections heading',
            content='Unique content string',
        )
        self.selenium.get('{}{}'.format(self.live_server_url, '/'))

    def test_intro_text_is_correct(self):
        """The page should include large introduction text."""
        intro_text = self.selenium.find_element_by_css_selector(
            "h3#lead-text").text
        self.assertEqual(
            intro_text, self.content.intro_text,
            "The Intro Text is Incorrect.")

    def test_content_header_is_correct(self):
        """The content's header should be set by the HomepageContent."""
        header = self.selenium.find_element_by_css_selector(
            "h4.homepage-heading").text
        self.assertEqual(
            header, self.content.content_title,
            "The Custom Content Section's Header is Incorrect.")

    def test_custom_content_is_correct(self):
        """The content should be set by the HomepageContent."""
        content = self.selenium.find_element_by_css_selector(
            '#homepage-custom-content').text
        self.assertIn(self.content.content, content,
                      'Custom content not found in section')

    def test_new_communities_are_shown(self):
        """The 3 newest communities are shown."""
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        community1 = Community.objects.create(
            title='Kalamazoo', date_joined=today)
        community2 = Community.objects.create(
            title='Kirtan', date_joined=today)
        community3 = Community.objects.create(
            title='Oslard', date_joined=today)
        hidden = Community.objects.create(
            title='Jugulum', date_joined=yesterday)

        self.selenium.get('{}{}'.format(self.live_server_url, '/'))
        html_excluding_footer = self.selenium.find_element_by_css_selector(
            '*:not(footer) > .container > .row').text
        self.assertNotIn(hidden.title, html_excluding_footer,
                         'Old community found on page.')

        communities = self.selenium.find_element_by_css_selector(
            'div#newest-communities').text
        self.assertIn(community1.title, communities, 'Community not in block.')
        self.assertIn(community2.title, communities, 'Community not in block.')
        self.assertIn(community3.title, communities, 'Community not in block.')

    def test_latest_news_is_shown(self):
        """The latest blog post is shown."""
        blog_post = BlogPost.objects.create(
            title='Hank Aaron the 24th', status=CONTENT_STATUS_PUBLISHED,
            user=self.user)
        self.selenium.refresh()

        html = self.selenium.find_element_by_css_selector('html').text
        self.assertIn(blog_post.title, html)

    def test_can_hide_communities_block(self):
        """The Newest Communities block can be hidden."""
        community = Community.objects.create(title='Kalamazoo')
        self.content.show_newest_communities = False
        self.content.save()
        self.selenium.refresh()

        html_excluding_footer = self.selenium.find_element_by_css_selector(
            '*:not(footer) > .container > .row').text
        self.assertNotIn(community.title, html_excluding_footer,
                         'Newest communities not hidden.')

    def test_can_hide_news_block(self):
        """The Latest News block can be hidden."""
        blog_post = BlogPost.objects.create(
            title='Hank Aaron the 24th', status=CONTENT_STATUS_PUBLISHED,
            user=self.user)
        self.content.show_news = False
        self.content.save()
        self.selenium.refresh()

        html = self.selenium.find_element_by_css_selector('html').text
        self.assertNotIn(blog_post.title, html, 'News was not hidden.')

    def test_no_blocks_widens_content(self):
        """Hiding the News & Communiits Blocks widens the Custom Content."""
        self.content.show_news = False
        self.content.show_newest_communities = False
        self.content.save()
        self.selenium.refresh()

        self.assertTrue(self.selenium.find_element_by_css_selector(
            '#homepage-custom-content.col-md-12'
        ), 'Custom content block not widened.')
