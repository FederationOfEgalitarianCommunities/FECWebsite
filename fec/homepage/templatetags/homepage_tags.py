"""Homepage tags that provide functionality for the HomepageContent model."""
from django import template

from ..models import HomepageContent


register = template.Library()


@register.assignment_tag
def get_homepage_content():
    """Return the site's HomepageContent."""
    content, _ = HomepageContent.objects.get_or_create()
    return content
