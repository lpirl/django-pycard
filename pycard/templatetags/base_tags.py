from random import randint

from django import template

from pycard.models import Configuration, MenuItem

register = template.Library()

def squares():

    def square_properties_generator():

        conf_get_int = Configuration.get_int
        height_min = conf_get_int('squares_height_min')
        height_max = conf_get_int('squares_height_max')
        width_min = conf_get_int('squares_width_min')
        width_max = conf_get_int('squares_width_max')

        for _ in range(conf_get_int('squares_count')):

            height = randint(height_min, height_max)
            width = randint(width_min, width_max)

            yield {
                'height':    height,
                'width':    width,
                'left':        randint(0, 100) - width/2,
                'top':        randint(0, 100) - height/2
            }

    return {
        'squares': square_properties_generator()
    }
register.inclusion_tag('squares.html')(squares)

def menu(article=None):
    items = MenuItem.objects.filter(root_article__hide=False)

    if bool(article):
        parents = article.parents()
        parents.append(article)

        # mark the menu item that is closest to the selected article:
        parents.reverse()
        for parent in parents:
            if parent in parents:
                items = items.extra(
                    select={
                        'active': "root_article_id = '%s'" % parent.id
                    }
                )
                break

    return {
        'vertically_center': not bool(article),
        'items': items
    }
register.inclusion_tag('menu.html')(menu)

def subarticles_list(sub_articles):
    return {
        'sub_articles': sub_articles
    }
register.inclusion_tag('subarticles_list.html')(subarticles_list)
