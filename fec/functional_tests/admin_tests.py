"""This module contains functional tests applicable to the Admin Backend."""
from core.utils import SeleniumTestCase


class GeneralAdminPageTests(SeleniumTestCase):
    """Test General Expectations for Every Admin Page."""
    def setUp(self):
        """Visit the admin page and login."""
        self.create_admin_and_login()

    def test_page_title_contains_the_fec(self):
        """The page title should end in `FEC Admin`."""
        expected = "| FEC Admin"
        page_title_suffix = self.selenium.title[-len(expected):]
        self.assertEqual(expected, page_title_suffix)

    def test_nav_header_is_correct(self):
        """The navigation's heading should be `The FEC`."""
        nav_header = self.selenium.find_element_by_class_name('admin-title')
        self.assertEqual("THE FEC", nav_header.text)


class CommunityAdminPageTests(SeleniumTestCase):
    """Test Expectations for the Community Admin Pages."""
    def setUp(self):
        """Visit the admin page and login."""
        self.create_admin_and_login()

    def test_community_link_is_in_the_admin_menu(self):
        """A link to modify Communities should be under Content in the menu."""
        content_menu = self.selenium.find_element_by_link_text("Content")
        content_submenu = content_menu.parent.find_element_by_css_selector(
            "ul.dropdown-menu-menu")
        self.assertIn("Communities", content_submenu.text)

    def test_publishing_fieldset_is_hidden_by_default(self):
        """The publishing fieldset should exist and be hidden by default."""
        self.selenium.find_element_by_link_text("Communities").click()
        self.selenium.find_element_by_link_text("Add community").click()
        fieldset_headers = self.selenium.find_elements_by_css_selector(
            "fieldset.collapse-closed h2.collapse-toggle")
        self.assertIn("Publishing", [fh.text for fh in fieldset_headers])

    def test_contact_fieldset_is_hidden_by_default(self):
        """The contact fieldset should exist and be hidden by default."""
        self.selenium.find_element_by_link_text("Communities").click()
        self.selenium.find_element_by_link_text("Add community").click()
        fieldset_headers = self.selenium.find_elements_by_css_selector(
            "fieldset.collapse-closed h2.collapse-toggle")
        self.assertIn("Contact", [fh.text for fh in fieldset_headers])
