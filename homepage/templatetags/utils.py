import os
import re

import requests
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


@register.simple_tag
def pypas_cli_version() -> str:
    NOT_AVAILABLE = 'NA'
    try:
        response = requests.get(settings.PYPAS_CLI_PYPI_URL)
    except Exception:
        return NOT_AVAILABLE
    if m := re.search(r'pypas-cli (\d+\.\d+\.\d+)', response.content.decode()):
        return m.group(1)
    return NOT_AVAILABLE
