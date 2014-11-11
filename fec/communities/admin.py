"""This module contains Admin Forms for :mod:`communities.models`."""
from django.contrib import admin
from django.utils.html import format_html
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin

from .models import Community, CommunityImage, CommunityFeed


class CommunityImageInline(TabularDynamicInlineAdmin):
    """An Inline Table Row representing a :class:`~.models.CommunityImage`."""
    model = CommunityImage


class CommunityFeedInline(TabularDynamicInlineAdmin):
    """An Inline Table Row representing a :class:`~.models.CommunityFeed`."""
    model = CommunityFeed


def get_community_email(obj):
    """Return the Community's :attr:`~.models.Community.email` as a link."""
    return format_html(
        '<a href="mailto:{0}" target="_blank">{0}</a>'.format(obj.email))

get_community_email.admin_order_field = 'email'
get_community_email.allow_tags = True
get_community_email.short_description = "Email"


class CommunityAdmin(DisplayableAdmin):
    """Represents the :class:`~.models.Community` model in the admin backend.

    .. attribute:: fieldsets

        Separate the publishing options from the general fields and add a
        ``Contact`` section.

    """
    inlines = (CommunityFeedInline, CommunityImageInline)
    list_display = ('title', 'is_community_in_dialog', 'general_location',
                    get_community_email, 'status', 'admin_link')
    list_filter = ('is_community_in_dialog', 'status', 'keywords__keyword')
    search_fields = ['title', 'general_location', 'year_founded', 'address']
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
