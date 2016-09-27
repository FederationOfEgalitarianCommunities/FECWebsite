'''This module determines the overall URL structure of the site.'''
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from django_nyt.urls import get_pattern as get_nyt_patterns
from wiki.urls import get_pattern as get_wiki_pattern


urlpatterns = i18n_patterns(
    "",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    url("^$", "homepage.views.index", name="home"),

    ("^communities/", include("communities.urls")),
    ("^systems-and-structures/", include("documents.urls")),

    url(r'^notifications/', get_nyt_patterns()),
    url(r'^wiki/', get_wiki_pattern()),

    ("^", include("mezzanine.urls")),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
