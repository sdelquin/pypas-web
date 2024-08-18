import os

from django import template
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def hashed_static(static_path: str) -> str:
    """
    Hashed static.
    Inspiration: https://www.reddit.com/r/django/comments/ychowr/comment/itqnrvv/
    """
    url_path = static(static_path)
    if settings.DEBUG:
        return url_path
    fs_path = find(static_path)
    last_modification = os.path.getmtime(fs_path)
    return f'{url_path}?v={last_modification}'
