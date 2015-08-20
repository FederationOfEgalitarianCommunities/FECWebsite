"""This module controls the URL routing for the ``documents`` package."""
from django.conf.urls import patterns, url

from .views import (DocumentDetail, DocumentCategoryDetail,
                    RootDocumentCategoryList, DocumentTagList)


urlpatterns = patterns(
    '',

    url(r'^$',
        RootDocumentCategoryList.as_view(),
        name="document_category_list"),

    url(r'^(?P<slug>[-_\w]+)/$',
        DocumentDetail.as_view(),
        name="document_detail"),

    url(r'^category/(?P<slug>[-_\w]+)/$',
        DocumentCategoryDetail.as_view(),
        name="document_category_detail"),

    url(r'^tag/(?P<tag>.*)/$',
        DocumentTagList.as_view(),
        name="document_tag_list"),

)
