from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, named_url):
    try:
        pattern = reverse(named_url)
    except NoReverseMatch:
        pattern = named_url
    path = context['request'].path
    return 'active' if path == pattern else''