"""This module contains functional tests applicable for every Page."""
from mezzanine.core.templatetags.mezzanine_tags import thumbnail
from mezzanine.pages.models import Link, Page, RichTextPage
from selenium.webdriver.common.keys import Keys

from communities.models import Community, CommunityImage
from core.utils import SeleniumTestCase
from homepage.models import HomepageContent


class GeneralPageTests(SeleniumTestCase):
    """Test General Expectations for Every Page."""
    def setUp(self):
        """Create two pages and visit one."""
        Link.objects.create(title="Blog", in_menus=[1, 2])
        self.rich_page = RichTextPage.objects.create(
            title='Visit', content='Visit us', in_menus=[1, 2])
        self.selenium.get(
            self.live_server_url + self.rich_page.get_absolute_url())

    def test_title_contains_fec_full_name(self):
        """The title should contain the FEC's full name."""
        self.assertIn('Federation of Egalitarian Communities',
                      self.selenium.title)

    def test_title_links_to_homepage(self):
        """The title should be a link to the Home Page."""
        title_link = self.selenium.find_element_by_css_selector(
            '#site-logo-title a:not(.pull-left)').text
        self.assertIn('Federation of\nEgalitarian Communities',
                      title_link,
                      'Did not find site name in header link.')

    def test_mobile_title_links_to_homepage(self):
        """The title on a mobile screen should be a link to the Home Page."""
        self.selenium.set_window_size(320, 568)
        title_link = self.selenium.find_element_by_css_selector(
            '#site-logo-title-xs a')
        self.assertTrue(title_link.is_displayed(),
                        'The mobile title is not displayed.')
        self.assertIn('Federation of Egalitarian Communities',
                      title_link.text,
                      'Did not find site name in header link.')

    def test_tagline_is_visible_and_correct_on_large_screens(self):
        """The tagline should be the FEC's slogan."""
        self.selenium.set_window_size(1680, 1050)
        tagline = self.selenium.find_element_by_css_selector(
            "#site-tagline")
        self.assertTrue(tagline.is_displayed(),
                        "The tagline is not displayed.")
        self.assertEqual(tagline.text, "A new way of living is possible.",
                         "The tagline is not correct.")

    def test_search_model_dropdown_is_removed(self):
        """The Search's `Model Dropdown` input should be removed."""
        self.assertElementDoesNotExist(
            self.selenium.find_element_by_xpath,
            "//form[@role='search']/div/select[@name='type']")

    def test_home_link_in_navigation_is_removed(self):
        """The Home link in the navigation bar should be removed."""
        self.assertElementDoesNotExist(
            self.selenium.find_element_by_css_selector,
            "ul.nav li#dropdown-menu-home")

    def test_home_link_in_left_sidebar_is_removed(self):
        """The Home link in the sidebar should be removed."""
        self.assertElementDoesNotExist(
            self.selenium.find_element_by_css_selector,
            "ul.nav li#tree-menu-home")

    def test_left_sidebar_is_removed(self):
        """The left sidebar should be removed."""
        self.assertElementDoesNotExist(
            self.selenium.find_element_by_css_selector,
            "div.container div.row div.col-md-2.left")

    def test_main_content_is_correct_size(self):
        """The main content should be the correct size."""
        main_content = self.selenium.find_elements_by_css_selector(
            "div.container div.row div.col-md-9.middle")
        self.assertEqual(len(main_content), 1,
                         "The middle content is not the correct column size.")

    def test_pages_contain_conference_info(self):
        """
        The general Pages(not blog posts, documents or communities) should
        contain the HomepageContent's communities_conference_text.
        """
        homepage, _ = HomepageContent.objects.get_or_create()
        homepage.communities_conference_text = (
            "This string has a uniqueness rating of over 9000")
        homepage.save()
        self.selenium.refresh()

        html = self.selenium.find_element_by_tag_name('html').text
        self.assertIn(homepage.communities_conference_text, html,
                      'Could not find Conference text on Page.')
        self.assertIn('Communities Conference', html,
                      'Could not find Conference header text on Page.')

    def test_blank_conference_info_is_hidden(self):
        """
        The Community Conference Information widget should be hidden if empty.
        """
        homepage, _ = HomepageContent.objects.get_or_create()
        homepage.communities_conference_text = ""
        homepage.save()
        self.selenium.refresh()

        html = self.selenium.find_element_by_tag_name('html').text
        self.assertNotIn('Communities Conference', html,
                         'Found Conference header text on Page.')


class FooterTests(SeleniumTestCase):
    """Test Expectations for the Page Footer."""
    def setUp(self):
        """Create a page & community and visit the home page."""
        Link.objects.create(title="Blog", in_menus=[1, 2])
        self.darmok = Community.objects.create(
            title="Darmok", number_of_adults=4, number_of_children=20,
            full_description="This is the description.")
        self.darmok_gallery_image = CommunityImage.objects.create(
            community=self.darmok, file="Test")
        self.selenium.get(self.live_server_url + '/')

    def test_default_footer_content_is_removed(self):
        """The default footer content should be removed."""
        footer = self.selenium.find_element_by_tag_name("footer")
        self.assertNotIn("Powered by Mezzanine and Django", footer.text)
        self.assertNotIn("Theme by Bootstrap", footer.text)

    def test_community_spotlight_information_is_correct(self):
        """The Community Spotlight should contain the correct information."""
        spotlight = self.selenium.find_element_by_css_selector(
            '#footer-community-spotlight')
        self.assertIn(self.darmok.title, spotlight.text)
        self.assertIn(str(self.darmok.number_of_adults), spotlight.text)
        self.assertIn(str(self.darmok.number_of_children), spotlight.text)
        self.assertIn(self.darmok.full_description, spotlight.text)

    def test_community_spotlight_requires_description(self):
        """
        The Community Spotlight should not display Communities without
        descriptions.
        """
        self.darmok.full_description = ''
        self.darmok.save()
        self.selenium.refresh()
        self.assertElementDoesNotExist(
            self.selenium.find_element_by_css_selector,
            '#footer-community-spotlight')

    def test_random_community_photo_exists(self):
        """A random Community's Gallery Image should be shown."""
        image = self.selenium.find_element_by_css_selector(
            "#footer-random-photo img")
        thumbnail_url = thumbnail(self.darmok_gallery_image, 360, 215)
        self.assertEqual(self.live_server_url + '/static/media/' +
                         thumbnail_url,
                         image.get_attribute("src"))

    def test_fic_link_exists(self):
        """A link to the FIC website should exist."""
        fic_link = self.selenium.find_element_by_css_selector("#fic-link")
        self.assertEqual("http://www.ic.org/", fic_link.get_attribute("href"))

    def test_footer_copyright_exists(self):
        """The copyright notice should be correct."""
        footer = self.selenium.find_element_by_tag_name("footer")
        self.assertIn(u"1999\u20132015", footer.text)


class SearchResultsPageTests(SeleniumTestCase):
    """Test General Expectations for the Search Results Page."""
    def setUp(self):
        """Create a Community and visit the home page."""
        Community.objects.create(title="sentry")
        self.selenium.get(self.live_server_url + '/')

    def test_empty_results_doesnt_contain_search_type(self):
        """The search type should not be displayed when no results exist."""
        query_box = self.selenium.find_element_by_css_selector(
            'input[name="q"]')
        query_box.send_keys("no result")
        query_box.send_keys(Keys.RETURN)

        content = self.selenium.find_element_by_css_selector(".middle p")
        self.assertNotIn("Everything", content.text)

    def test_results_dont_contain_search_type(self):
        """The search type should not be displayed when results exist."""
        query_box = self.selenium.find_element_by_css_selector(
            'input[name="q"]')
        query_box.send_keys("sentry")
        query_box.send_keys(Keys.RETURN)

        content = self.selenium.find_element_by_css_selector(".middle p")
        self.assertNotIn("Everything", content.text)
