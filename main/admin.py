from django.contrib.admin import site, ModelAdmin
from django.forms import ModelForm
from django.forms.widgets import Textarea
from main.models import (MenuItem, Article, Attachment, Configuration,
                         ContentMedia)

from django.contrib import admin

class ArticleAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        self.fields['teaser'].widget = admin.widgets.AdminTextareaWidget()

class ArticleAdmin(ModelAdmin):
    list_display = ('__unicode__', 'teaser', 'parent', 'date_modified')
    form = ArticleAdminForm

site.register(MenuItem, ModelAdmin)
site.register(Article, ArticleAdmin)
site.register(Attachment, ModelAdmin)
site.register(Configuration, ModelAdmin)
site.register(ContentMedia, ModelAdmin)
