# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Article.teaser'
        db.alter_column(u'pycard_article', 'teaser', self.gf('django.db.models.fields.CharField')(max_length=1024))

    def backwards(self, orm):

        # Changing field 'Article.teaser'
        db.alter_column(u'pycard_article', 'teaser', self.gf('django.db.models.fields.CharField')(max_length=256))

    models = {
        u'pycard.article': {
            'Meta': {'ordering': "['-sort_priority']", 'object_name': 'Article'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pycard.Attachment']", 'symmetrical': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_media': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pycard.ContentMedia']", 'symmetrical': 'False', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'hide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['pycard.Article']"}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'sort_priority': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'sub_articles_list_bottom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_articles_list_top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'teaser': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'pycard.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'data': ('django.db.models.fields.files.FileField', [], {'max_length': '256'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'pycard.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'pycard.contentmedia': {
            'Meta': {'object_name': 'ContentMedia'},
            'data': ('django.db.models.fields.files.FileField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pycard.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos_x': ('django.db.models.fields.IntegerField', [], {}),
            'pos_y': ('django.db.models.fields.IntegerField', [], {}),
            'root_article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['pycard.Article']"}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['pycard']