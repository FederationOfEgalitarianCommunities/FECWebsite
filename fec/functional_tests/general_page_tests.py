"""This module contains functional tests applicable for every Page."""
from selenium.common.exceptions import NoSuchElementException

from core.utils import SeleniumTestCase


class GeneralPageTests(SeleniumTestCase):
    """Test General Expectations for Every Page."""
    def setUp(self):
        """Visit the home page."""
        self.selenium.get('{}{}'.format(self.live_server_url, '/'))

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
        self.assertTrue(tagline.is_displayed(), "The tagline is not displayed.")
        self.assertEqual(tagline.text, "A new way of living is possible.",
                         "The tagline is not correct.")

    def test_search_model_dropdown_is_removed(self):
        """The Search's `Model Dropdown` input should be removed."""
        self.assertRaises(NoSuchElementException,
                          self.selenium.find_element_by_xpath,
                          "//form[@role='search']/div/select[@name='type']")

    def test_left_sidebar_is_removed(self):
        """The left sidebar should be removed and the main content expanded."""
        self.assertRaises(NoSuchElementException,
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
        self.assertIn("Copyright 1999-", footer.text)
