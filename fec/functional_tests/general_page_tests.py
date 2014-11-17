"""This module contains functional tests applicable for every Page."""
from mezzanine.pages.models import Link

from core.utils import SeleniumTestCase


class GeneralPageTests(SeleniumTestCase):
    """Test General Expectations for Every Page."""
    def setUp(self):
        """Create a page and visit the home page."""
        Link.objects.create(title="Blog", in_menus=[1, 2, 3])
        self.selenium.get(self.live_server_url + '/')

    def test_title_contains_fec_full_name(self):
        """The title should contain the FEC's full name."""
        self.assertIn('Federation of Egalitarian Communities',
                      self.selenium.title)

    def test_tagline_is_hidden_on_small_screens(self):
        """The tagline should not be visible on small screens."""
        self.selenium.set_window_size(300, 150)
        tagline = self.selenium.find_element_by_css_selector(
            "div.navbar-header p.navbar-text")
        self.assertFalse(tagline.is_displayed(), "The tagline is displayed.")

    def test_tagline_is_visible_and_correct_on_large_screens(self):
        """The tagline should be the FEC's slogan."""
        self.selenium.set_window_size(1680, 1050)
        tagline = self.selenium.find_element_by_css_selector(
            "div.navbar-header p.navbar-text")
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
        """The Home link in the left sidebar should be removed."""
        self.assertElementDoesNotExist(
            self.selenium.find_element_by_css_selector,
            "ul.nav li#tree-menu-home")

    def test_right_sidebar_is_removed(self):
        """The right sidebar should be removed and main content expanded."""
        self.assertElementDoesNotExist(
            self.selenium.find_element_by_css_selector,
            "div.container div.row div.col-md-3.right")
        main_content = self.selenium.find_elements_by_css_selector(
            "div.container div.row div.col-md-10.middle")
        self.assertEqual(len(main_content), 1,
                         "The middle content is not the correct column size.")

    def test_default_footer_content_is_removed(self):
        """The default footer content should be removed."""
        footer = self.selenium.find_element_by_tag_name("footer")
        self.assertNotIn("Powered by Mezzanine and Django", footer.text)
        self.assertNotIn("Theme by Bootstrap", footer.text)

    def test_footer_copyright_exists(self):
        """The copyright notice in the footer should be correct."""
        footer = self.selenium.find_element_by_tag_name("footer")
        self.assertIn(u"1999 \u2013 2014", footer.text)
