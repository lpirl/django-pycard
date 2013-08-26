# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Configuration'
        db.create_table(u'pycard_configuration', (
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'pycard', ['Configuration'])

        # Adding model 'MenuItem'
        db.create_table(u'pycard_menuitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pos_x', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_y', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('root_article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['pycard.Article'])),
        ))
        db.send_create_signal(u'pycard', ['MenuItem'])

        # Adding model 'Article'
        db.create_table(u'pycard_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['pycard.Article'])),
            ('teaser', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('sub_articles_list_top', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sub_articles_list_bottom', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hide', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pycard', ['Article'])

        # Adding M2M table for field attachments on 'Article'
        m2m_table_name = db.shorten_name(u'pycard_article_attachments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'pycard.article'], null=False)),
            ('attachment', models.ForeignKey(orm[u'pycard.attachment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'attachment_id'])

        # Adding M2M table for field content_media on 'Article'
        m2m_table_name = db.shorten_name(u'pycard_article_content_media')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'pycard.article'], null=False)),
            ('contentmedia', models.ForeignKey(orm[u'pycard.contentmedia'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'contentmedia_id'])

        # Adding model 'Attachment'
        db.create_table(u'pycard_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('data', self.gf('django.db.models.fields.files.FileField')(max_length=256)),
        ))
        db.send_create_signal(u'pycard', ['Attachment'])

        # Adding model 'ContentMedia'
        db.create_table(u'pycard_contentmedia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.files.FileField')(max_length=256)),
        ))
        db.send_create_signal(u'pycard', ['ContentMedia'])


    def backwards(self, orm):
        # Deleting model 'Configuration'
        db.delete_table(u'pycard_configuration')

        # Deleting model 'MenuItem'
        db.delete_table(u'pycard_menuitem')

        # Deleting model 'Article'
        db.delete_table(u'pycard_article')

        # Removing M2M table for field attachments on 'Article'
        db.delete_table(db.shorten_name(u'pycard_article_attachments'))

        # Removing M2M table for field content_media on 'Article'
        db.delete_table(db.shorten_name(u'pycard_article_content_media'))

        # Deleting model 'Attachment'
        db.delete_table(u'pycard_attachment')

        # Deleting model 'ContentMedia'
        db.delete_table(u'pycard_contentmedia')


    models = {
        u'pycard.article': {
            'Meta': {'object_name': 'Article'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pycard.Attachment']", 'symmetrical': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_media': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pycard.ContentMedia']", 'symmetrical': 'False', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'hide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['pycard.Article']"}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'sub_articles_list_bottom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_articles_list_top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'teaser': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
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