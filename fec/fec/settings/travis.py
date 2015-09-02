import os

from .test import *


sauce_username = os.environ['SAUCE_USERNAME']
sauce_access_key = os.environ['SAUCE_ACCESS_KEY']
SELENIUM_SERVER = "http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(
    sauce_username, sauce_access_key)
SELENIUM_CAPABILITIES['tunnelIdentifier'] = os.environ['TRAVIS_JOB_NUMBER']
SELENIUM_CAPABILITIES['build'] = os.environ["TRAVIS_BUILD_NUMBER"]
SELENIUM_CAPABILITIES['tags'] = [os.environ["TRAVIS_PYTHON_VERSION"], "CI"]
