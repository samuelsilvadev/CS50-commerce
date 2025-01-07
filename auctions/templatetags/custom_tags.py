from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def active_class(context, url_name):
    """
    Returns 'active' if the current request path matches the given URL name.
    """
    request = context["request"]

    if request.path == reverse(url_name):
        return "active"
    return ""
