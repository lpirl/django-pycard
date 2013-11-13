# encoding: utf-8
from os.path import splitext, basename
from random import randint

from django import template
register = template.Library()

@register.assignment_tag
def is_path_to_image(path):
    """
    Returns true, if ``path`` points to an image.
    (Trivially checks extension)
    """
    return splitext(path)[1][1:].lower() in ("jpg", "jpeg", "png")

@register.simple_tag
def random_int(minimum, maximum):
    """
    Returns a random integer x with minimum <= x <= maximum.
    """
    return randint(minimum, maximum)

@register.simple_tag
def filename(path):
    """
    Returns the file name in ``path`` without the extension.
    """
    return splitext(basename(path))[0]
