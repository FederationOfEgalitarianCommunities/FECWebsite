"""This module contains functional tests for the Home Page."""
from core.utils import SeleniumTestCase


class HomePageTests(SeleniumTestCase):
    """Test Expectations for the Home Page."""
    def setUp(self):
        """Visit the home page."""
        self.selenium.get('{}{}'.format(self.live_server_url, '/'))

    def test_content_header_is_correct(self):
        """The content's header should welcome the user to the FEC website."""
        header = self.selenium.find_element_by_css_selector(".middle h2")
        self.assertEqual(
            header.text,
            "Welcome to the Federation of Egalitarian Communities!"
        )

    def test_content_has_introduction(self):
        """The content should include an introduction to the FEC."""
        content = self.selenium.find_element_by_css_selector(".middle")
        self.assertIn("The FEC is a union of egalitarian communities",
                      content.text)
