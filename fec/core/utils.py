from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from django.test import LiveServerTestCase


class SeleniumTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME)
        cls.selenium.implicitly_wait(3)
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()
