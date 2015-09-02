import os

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .base import *


# Remove development/debugging apps
OPTIONAL_APPS = (
    'compressor',
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)
COMPRESS_ENABLED = True

# Use a less intense password hasher
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

# Allow liveservers on multiple ports in case running in parallel
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8081-8099'

SELENIUM_SERVER = "http://127.0.0.1:4444/wd/hub"
SELENIUM_CAPABILITIES = DesiredCapabilities.CHROME.copy()

# Use an in-memory SQLite database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# Disable the cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
