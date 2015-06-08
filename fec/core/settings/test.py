from .base import *

SOUTH_TESTS_MIGRATE = False

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-branches',
    '--cover-package=communities,documents,homepage',
    '--with-progressive',
    '--with-watcher',
    '--filetype=.css',
    '--filetype=.html',
    '--filetype=.js',
    '--filetype=.less',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory://testdb',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
