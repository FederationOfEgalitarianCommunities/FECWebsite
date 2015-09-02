import os

from .test import *

if 'TRAVIS' in os.environ:
    sauce_username = os.environ['SAUCE_USERNAME']
    sauce_access_key = os.environ['SAUCE_ACCESS_KEY']
    SELENIUM_SERVER = "http://{}:{}@localhost:4445/wd/hub".format(
        sauce_username, sauce_access_key)
    SELENIUM_CAPABILITIES['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
    SELENIUM_CAPABILITIES['build'] = os.environ["TRAVIS_BUILD_NUMBER"]
    SELENIUM_CAPABILITIES['tags'] = [os.environ["TRAVIS_PYTHON_VERSION"], "CI"]
