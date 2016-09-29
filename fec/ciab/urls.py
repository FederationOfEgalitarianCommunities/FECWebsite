"""This module controls the URL routing for the ``ciab`` package."""
from django.conf.urls import patterns, url

from .views import decision_detail_view


urlpatterns = patterns(
    '',
    url(r'^$', decision_detail_view, name='decision_detail_view'),
)
