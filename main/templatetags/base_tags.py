from random import randint

from django import template

from main.models import Configuration

register = template.Library()

def generate_squares():

	conf_get_int = Configuration.get_int
	height_min = conf_get_int('squares_height_min')
	height_max = conf_get_int('squares_height_max')
	width_min = conf_get_int('squares_width_min')
	width_max = conf_get_int('squares_width_max')

	def square_properties_generator():

		for _ in range(conf_get_int('squares_count')):

			height = randint(height_min, height_max)
			width = randint(width_min, width_max)
			left = randint(0, 100) - width/2
			top = randint(0, 100) - height/2

			yield {
				'height': height,
				'width': width,
				'top': top,
				'left': left
			}

	return {
		'squares': square_properties_generator()
		}
register.inclusion_tag('squares.html')(generate_squares)
