# encoding: utf-8
from os.path import splitext, basename

from django import template
register = template.Library()

@register.simple_tag
def filename(path):
    """
    Returns the file name in ``path`` without the extension.
    """
    return splitext(basename(path))[0]
