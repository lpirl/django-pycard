from django import template
register = template.Library()

from main.models import Configuration

@register.simple_tag
def get_configuration_str(key):
    return Configuration.get_str(key)
