from __future__ import absolute_import, unicode_literals
import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


######################
# FEC Customizations #
######################

# Utility Functions
def get_env_variable(var_name):
    """Get the environmental variable or raise an exception."""
    try:
        return os.environ.get(var_name)
    except KeyError:
        error_msg = "Set the {0} environmental variable.".format(var_name)
        raise ImproperlyConfigured(error_msg)


# Title & Tagline
SITE_TITLE = "Federation of Egalitarian Communities"
SITE_TAGLINE = "A new way of living is possible."

# Base in Eastern Time
TIME_ZONE = 'America/New_York'

# Remove the Model-dropdown for the search
SEARCH_MODEL_CHOICES = ()

# Bump up Posts per Page
BLOG_POST_PER_PAGE = 10
# Turn on featured images for blog posts.
BLOG_USE_FEATURED_IMAGE = True

# Remove Ratings from Comments
COMMENTS_USE_RATINGS = False

# Add custom apps
INSTALLED_APPS = (
    "fec",
    "communities",
    "documents",
    "homepage",

    "axes",
    "email_obfuscator",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.pages",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.galleries",
    # "mezzanine.accounts",
    # "mezzanine.mobile",
)

# Add Custom Apps to Admin Menu
ADMIN_MENU_ORDER = (
    ("Content",
        ("communities.Community",
         ("Homepage", "homepage.HomepageContent"),
         "pages.Page",
         "blog.BlogPost",
         "generic.ThreadedComment",
         ("Media Library", "fb_browse"),
         )
     ),
    ("Systems & Structures",
        ("documents.Document",
         "documents.DocumentCategory",
         ),
     ),
    ("Site",
        ("sites.Site",
         "redirects.Redirect",
         "conf.Setting",
         )
     ),
    ("Users",
        ("auth.User",
         "auth.Group",
         )
     ),
)

# Specify Settings Available in Templates
TEMPLATE_ACCESSIBLE_SETTINGS = (
    'MEDIA_URL',
    # Defaults
    'ACCOUNTS_APPROVAL_REQUIRED', 'ACCOUNTS_VERIFICATION_REQUIRED',
    'ADMIN_MENU_COLLAPSED', 'BITLY_ACCESS_TOKEN', 'BLOG_USE_FEATURED_IMAGE',
    'COMMENTS_DISQUS_SHORTNAME', 'COMMENTS_NUM_LATEST',
    'COMMENTS_DISQUS_API_PUBLIC_KEY', 'COMMENTS_DISQUS_API_SECRET_KEY',
    'COMMENTS_USE_RATINGS', 'DEV_SERVER', 'FORMS_USE_HTML5',
    'GRAPPELLI_INSTALLED', 'GOOGLE_ANALYTICS_ID', 'JQUERY_FILENAME',
    'JQUERY_UI_FILENAME', 'LOGIN_URL', 'LOGOUT_URL', 'SITE_TITLE',
    'SITE_TAGLINE', 'USE_L10N', 'USE_MODELTRANSLATION'
)

# Compile LESS Files using lessc
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

# Minify CSS
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]

# Always compile static files
COMPRESS_ENABLED = True

# Only use the Top Nav menu
PAGE_MENU_TEMPLATES = (
    (1, "Top navigation bar", "pages/menus/dropdown.html"),
)

# Set Secret Key via EnvVar
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")

# Allow all hosts; overridden in prod settings
ALLOWED_HOSTS = ['*']

# Lock out IPs after 10 failed login attempts
AXES_LOGIN_FAILURE_LIMIT = 10

# Lock out IPs for 24 hours
AXES_COOLOFF_TIME = 24


######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for conveniently
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content",
#          "pages.Page",
#          "blog.BlogPost",
#          "generic.ThreadedComment",
#          ("Media Library", "fb_browse"),
#          )
#      ),
#     ("Site",
#         ("sites.Site",
#          "redirects.Redirect",
#          "conf.Setting",
#          )
#      ),
#     ("Users",
#         ("auth.User",
#          "auth.Group",
#          )
#      ),
# )

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, _("Top navigation bar"), "pages/menus/dropdown.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         (_("Image"),),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         (_("Another name"),),
#         {"blank": True, "default": 1},
#     ),
# )

# Setting to turn on featured images for blog posts. Defaults to False.
#
# BLOG_USE_FEATURED_IMAGE = True

# If True, the django-modeltranslation will be added to the
# INSTALLED_APPS setting.
USE_MODELTRANSLATION = False


########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
# TIME_ZONE = 'UTC'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# Supported languages
LANGUAGES = (
    ('en', _('English')),
)

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.",
        # DB name or path to database file if using sqlite3.
        "NAME": "",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}


#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../')
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_APP

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)


################
# APPLICATIONS #
################

# INSTALLED_APPS = (
#     "core",
#     "communities",
#     "documents",
#     "homepage",
#
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.redirects",
#     "django.contrib.sessions",
#     "django.contrib.sites",
#     "django.contrib.sitemaps",
#     "django.contrib.staticfiles",
#     "mezzanine.boot",
#     "mezzanine.conf",
#     "mezzanine.core",
#     "mezzanine.generic",
#     "mezzanine.pages",
#     "mezzanine.blog",
#     "mezzanine.forms",
#     "mezzanine.galleries",
#     "mezzanine.twitter",
#     # "mezzanine.accounts",
#     # "mezzanine.mobile",
# )

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
    "mezzanine.pages.context_processors.page",
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    # Uncomment if using internationalisation or localisation
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.FailedLoginMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local_settings import *", we use exec so that
# local_settings has full access to everything defined in this module.

f = os.path.join(PROJECT_APP_PATH, "local_settings.py")
if os.path.exists(f):
    exec(open(f, "rb").read())


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
