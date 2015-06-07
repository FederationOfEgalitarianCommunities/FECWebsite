"""Use the :class:`mezzanine.core.admin.SingletonAdmin` form for admins."""
from django.contrib import admin

from mezzanine.core.admin import SingletonAdmin

from .models import HomepageContent


admin.site.register(HomepageContent, SingletonAdmin)
