from django.contrib.admin import site, ModelAdmin
from main.models import (MenuItem, Article, Attachment, Configuration,
                         ContentMedia)

class ArticleAdmin(ModelAdmin):
    list_display = ('__unicode__', 'teaser', 'parent', 'date_modified')

site.register(MenuItem, ModelAdmin)
site.register(Article, ArticleAdmin)
site.register(Attachment, ModelAdmin)
site.register(Configuration, ModelAdmin)
site.register(ContentMedia, ModelAdmin)
