from django.contrib.admin import site
from django.contrib.admin import ModelAdmin
from main.models import MenuItem, Article, Attachment, Configuration

site.register(MenuItem, ModelAdmin)
site.register(Article, ModelAdmin)
site.register(Attachment, ModelAdmin)
site.register(Configuration, ModelAdmin)
