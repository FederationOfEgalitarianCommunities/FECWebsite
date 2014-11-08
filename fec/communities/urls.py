"""This module controls the URL routing for the ``communities`` package."""
from django.conf.urls import patterns, url

from .views import (CommunityList, CommunityDetail, CommunityInDialogDetail)


urlpatterns = patterns(
    '',
    url(r'^$', CommunityList.as_view(),
        name='community_list'),

    url(r'^(?P<slug>[-_\w]+)/$', CommunityDetail.as_view(),
        name='community_detail'),
    url(r'^in-dialog/(?P<slug>[-_\w]+)/$',
        CommunityInDialogDetail.as_view(),
        name='community_in_dialog_detail'),
)
