from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_view_communities_and_community_details(self):

        # Ingrid has just heard about the Communities movement. She's an anarchist, so
        # she immediately goes to the FEC's home page.
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention the Federation of Egalitarian
        # Communities.
        self.assertIn('Federation of Egalitarian Communities', self.browser.title)
        self.fail("Finish the test!")

        # She clicks a link to list all the communities.

        # Interested, she clicks on the link to a community.

        # She can see the specific details of a community.


if __name__ == '__main__':
    unittest.main()
