# encoding: utf-8

from django.contrib.admin import site, ModelAdmin
from django.forms import ModelForm
from pycard.models import (MenuItem, Article, Attachment, Configuration,
                         ContentMedia)

from django.contrib import admin

class ArticleAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        self.fields['teaser'].widget = admin.widgets.AdminTextareaWidget()

class ArticleAdmin(ModelAdmin):
    class Media:
        css = {
            "all": ("admin.css",)
        }
    list_display = ('__unicode__', 'teaser', 'slug', 'parent',
                    'sort_priority', 'date_modified')
    ordering = ['-date_modified']
    form = ArticleAdminForm

site.register(MenuItem, ModelAdmin)
site.register(Article, ArticleAdmin)
site.register(Attachment, ModelAdmin)
site.register(Configuration, ModelAdmin)
site.register(ContentMedia, ModelAdmin)
