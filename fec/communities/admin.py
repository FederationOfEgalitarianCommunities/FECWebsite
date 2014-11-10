"""This module contains Admin Forms for :mod:`communities.models`."""
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin

from .models import Community, CommunityImage, CommunityFeed


class CommunityImageInline(TabularDynamicInlineAdmin):
    """An Inline Table Row representing a :class:`~.models.CommunityImage`."""
    model = CommunityImage


class CommunityFeedInline(TabularDynamicInlineAdmin):
    """An Inline Table Row representing a :class:`~.models.CommunityFeed`."""
    model = CommunityFeed


class CommunityAdmin(DisplayableAdmin):
    """Represents the :class:`~.models.Community` model in the admin backend.

    .. attribute:: fieldsets

        Separate the publishing options from the general fields and add a
        ``Contact`` section.

    """
    inlines = [CommunityFeedInline, CommunityImageInline]
    fieldsets = (
        (None, {
            "fields": [("title", "profile_image"),
                       ("short_description", "full_description"),
                       ("general_location", "year_founded"),
                       ("number_of_adults", "number_of_children"),
                       "is_community_in_dialog"],
        }),
        ("Contact", {
            "fields": ["address", "website", "email", "phone"],
            "classes": ("collapse-closed",)
        }),
        ("Publishing", {
            "fields":  ["status", ("publish_date", "expiry_date")],
            "classes": ("collapse-closed",)
        }),
        ("Meta data", {
            "fields": ["_meta_title", "slug",
                       ("description", "gen_description"),
                       "keywords", "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )

    class Media(object):
        """Include Mezzanine's Admin Gallery CSS."""
        css = {"all": ("mezzanine/css/admin/gallery.css",)}


admin.site.register(Community, CommunityAdmin)
