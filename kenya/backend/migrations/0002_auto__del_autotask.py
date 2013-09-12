# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AutoTask'
        db.delete_table('backend_autotask')


    def backwards(self, orm):
        # Adding model 'AutoTask'
        db.create_table('backend_autotask', (
            ('function', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('backend', ['AutoTask'])


    models = {
        'backend.automatedmessage': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'AutomatedMessage'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['backend.MessageGroup']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'next_message': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous_message'", 'null': 'True', 'to': "orm['backend.AutomatedMessage']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'send_base': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.MessageBase']", 'null': 'True', 'blank': 'True'}),
            'send_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'backend.condition': {
            'Meta': {'object_name': 'Condition', '_ormbases': ['backend.MessageGroup']},
            'messagegroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['backend.MessageGroup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'backend.email': {
            'Meta': {'object_name': 'Email'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '600'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'backend.languagegroup': {
            'Meta': {'object_name': 'LanguageGroup', '_ormbases': ['backend.MessageGroup']},
            'messagegroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['backend.MessageGroup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'backend.messagebase': {
            'Meta': {'object_name': 'MessageBase'},
            'display': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'backend.messagegroup': {
            'Meta': {'object_name': 'MessageGroup'},
            'display': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'backend.studygroup': {
            'Meta': {'object_name': 'StudyGroup', '_ormbases': ['backend.MessageGroup']},
            'messagegroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['backend.MessageGroup']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['backend']