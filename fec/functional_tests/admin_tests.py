"""This module contains functional tests applicable to the Admin Backend."""
from selenium.webdriver.common.keys import Keys

from core.utils import SeleniumTestCase


class GeneralAdminPageTests(SeleniumTestCase):
    """Test General Expectations for Every Admin Page."""
    def setUp(self):
        """Create an administrator, visit the admin page and login."""
        self.selenium.get(self.live_server_url + '/admin/')
        username_field = self.selenium.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.selenium.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

    def test_page_title_contains_the_fec(self):
        """The page title should end in `FEC Admin`."""
        expected = "| FEC Admin"
        page_title_suffix = self.selenium.title[-len(expected):]
        self.assertEqual(expected, page_title_suffix)

    def test_nav_header_is_correct(self):
        """The navigation's heading should be `The FEC`."""
        nav_header = self.selenium.find_element_by_class_name('admin-title')
        self.assertEqual("THE FEC", nav_header.text)
