from django.contrib.admin import site, ModelAdmin
from main.models import *

class ArticleAdmin(ModelAdmin):
	list_display = ('__unicode__', 'teaser', 'parent')

site.register(MenuItem, ModelAdmin)
site.register(Article, ArticleAdmin)
site.register(Attachment, ModelAdmin)
site.register(Configuration, ModelAdmin)
site.register(ContentMedia, ModelAdmin)


