"""This module contains utility functions used throughout the application."""
from StringIO import StringIO

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import transaction
from django.test import LiveServerTestCase
from PIL import Image
import pep8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class SeleniumTestCase(LiveServerTestCase):
    """A test case with a Selenium WebDriver and extra helper functions."""
    @classmethod
    def setUpClass(cls):
        """Create a new :class:`selenium.webdriver.Remote` Connection.

        The Selenium Server is expected to be running at
        ``http://127.0.0.1:4444/wd/hub`` and the ``Chrome`` webdriver is used.

        :returns: :obj:`None`

        """
        cls.selenium = webdriver.Remote(
            command_executor=settings.SELENIUM_SERVER,
            desired_capabilities=settings.SELENIUM_CAPABILITIES)
        cls.selenium.implicitly_wait(1)
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Close the Selenium Browser.

        :returns: :obj:`None`

        """
        cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def create_admin_and_login(self):
        """Create and Login as an Administrator.

        :returns: :obj:`None`

        """
        User.objects.create_superuser('admin', 'admin@test.test', 'admin')
        transaction.commit()
        self.selenium.get(self.live_server_url + '/admin/')
        username_field = self.selenium.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.selenium.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

    def assertTitleEquals(self, title):
        """Assert that the current page title is correct.

        Fails if the ``title`` is not equal to Selenium's current page title.

        The trailing ``SITE_TITLE`` is accounted for automatically and should
        not be included.

        :param title: The title to test for.
        :type title: :class:`String`

        """
        trailing_text = " | " + settings.SITE_TITLE
        self.assertEqual(title + trailing_text, self.selenium.title,
                         'The page title is not "{0}".'.format(title))

    def assertPageHeaderEquals(self, header):
        """Assert that the current page header is correct.

        Fails if the ``header`` is not equal to the first ``h1`` HTML tag.

        :param header: The header to test for.
        :type header: :class:`String`

        """
        header_element = self.selenium.find_element_by_css_selector("h1")
        self.assertEqual(
            header, header_element.text,
            'The page header is not equal to "{0}"'.format(header))

    def assertElementDoesNotExist(self, selector_function, *args):
        """Assert that an element does not exist on the current page.

        Fails if the element represented by the ``selector_function`` applied
        to ``args`` does not raise a
        :class:`~selenium.common.exceptions.NoSuchElementException`.

        :param selector_function: The Selenium Element selector function to be
                                  called with the other arguments.
        :type selector_function: function

        """
        self.assertRaises(NoSuchElementException, selector_function, *args)

    def assertItemIsInAdminMenu(self, item_name, sub_menu):
        """Assert that an item is in the specified admin sub menu.

        :param item_name: The name of the menu item. E.g., Pages, Comments.
        :type item_name: string
        :param sub_menu: The name of the admin sub menu. E.g., Content, Site.
        :type sub_menu: string

        """
        sub_menu_link = self.selenium.find_element_by_link_text(sub_menu)
        sub_menu_items = sub_menu_link.find_elements_by_xpath("../ul/li")
        print sub_menu_items
        self.assertTrue(any(item.text == item_name for item in sub_menu_items),
                        'Could not find the Menu Item "{0}" in the "{1}" Menu'.
                        format(item_name, sub_menu))

    def assertActiveBreadcrumbEquals(self, expected_text):
        """Assert that the expected_text is the active breadcrumb's text.

        :param expected_text: The expected text of the active breadcrumb.
        :type expected_text: string

        """
        active_crumb = self.selenium.find_element_by_css_selector(
            "ul.breadcrumb li.active")
        self.assertEqual(expected_text, active_crumb.text,
                         'The Active Breadcrumb Text was "{0}" instead of '
                         '"{1}"'.format(active_crumb.text, expected_text))

    def assertInactiveBreadcrumbEquals(self, expected_text):
        """Assert that the expected_text is an inactive breadcrumb."""
        breadcrumbs = self.selenium.find_elements_by_css_selector(
            "ul.breadcrumb li")
        inactive = [x for x in breadcrumbs if "active" not in
                    x.get_attribute("class")]
        self.assertTrue(any(crumb.text == expected_text for crumb in inactive),
                        'Could not find "{0}" in any breadcrumbs.'.format(
                            expected_text))


def create_test_image():
    """Create a 500x500px image for use in tests.

    :returns: :class:`django.core.files.base.ContentFile`

    """
    image_file = StringIO()
    image = Image.new('RGBA', size=(500, 500), color=(256, 0, 0))
    image.save(image_file, 'png')
    image_file.seek(0)

    return ContentFile(image_file.read(), 'test.png')
create_test_image.__test__ = False      # Nose thinks this is a test.


def check_pep8(file_list):
    """Ensure the files are PEP8 complaint."""
    pep8style = pep8.StyleGuide()
    return pep8style.check_files(file_list)
