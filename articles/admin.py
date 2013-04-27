from django.contrib.admin import site
from django.contrib.admin import ModelAdmin
from articles.models import MenuItem, Article, Attachment

site.register(MenuItem, ModelAdmin)
site.register(Article, ModelAdmin)
site.register(Attachment, ModelAdmin)
