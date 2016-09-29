from django.contrib import admin

from .models import (Decision, Option)


class DecisionAdmin(admin.ModelAdmin):
    model = Decision
    fields = ('name', 'short_description', 'long_description')


class OptionAdmin(admin.ModelAdmin):
    model = Option


admin.site.register(Decision, DecisionAdmin)
admin.site.register(Option, OptionAdmin)
