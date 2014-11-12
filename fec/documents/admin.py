"""This module contains Admin Forms for :mod:`documents.models`."""
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin

from .models import Document, DocumentCategory


class DocumentCategoryAdmin(admin.ModelAdmin):
    """Represents the :class:`~.models.DocumentCategory` model in the admin."""
    list_display = ('title', 'parent', '_order', 'admin_link',)
    list_filter = ('parent',)
    search_fields = ('title',)
    fieldsets = ((None, {'fields': ('title', 'parent', '_order')}),)

admin.site.register(DocumentCategory, DocumentCategoryAdmin)


class DocumentAdmin(DisplayableAdmin):
    """Represents the :class:`~.models.Document` model in the admin."""
    list_display = ('title', 'category', 'community', 'status', 'admin_link')
    list_filter = ('category', 'community', 'status',)
    search_fields = ('title', 'category', 'community',)
    fieldsets = (
        (None, {
            "fields": ["title", "category", "community", "contents",
                       "keywords", "status",
                       ("publish_date", "expiry_date")],
        }),
        ("Meta data", {
            "fields": ["_meta_title", "slug",
                       ("description", "gen_description"),
                       "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )

admin.site.register(Document, DocumentAdmin)
