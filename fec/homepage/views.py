"""Handles rendering of the Home Page."""
from django.shortcuts import render

from .models import HomepageContent


def index(request):
    """Render the site's Homepage."""
    homepage_content, _ = HomepageContent.objects.get_or_create()
    return render(request, "index.html",
                  {'homepage_content': homepage_content})
