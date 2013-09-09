# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AutomatedMessage'
        db.create_table('backend_automatedmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('send_base', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.MessageBase'], null=True, blank=True)),
            ('send_offset', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('next_message', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='previous_message', null=True, to=orm['backend.AutomatedMessage'])),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('backend', ['AutomatedMessage'])

        # Adding M2M table for field groups on 'AutomatedMessage'
        m2m_table_name = db.shorten_name('backend_automatedmessage_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('automatedmessage', models.ForeignKey(orm['backend.automatedmessage'], null=False)),
            ('messagegroup', models.ForeignKey(orm['backend.messagegroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['automatedmessage_id', 'messagegroup_id'])

        # Adding model 'MessageBase'
        db.create_table('backend_messagebase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('backend', ['MessageBase'])

        # Adding model 'MessageGroup'
        db.create_table('backend_messagegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('backend', ['MessageGroup'])

        # Adding model 'Condition'
        db.create_table('backend_condition', (
            ('messagegroup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backend.MessageGroup'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('backend', ['Condition'])

        # Adding model 'StudyGroup'
        db.create_table('backend_studygroup', (
            ('messagegroup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backend.MessageGroup'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('backend', ['StudyGroup'])

        # Adding model 'LanguageGroup'
        db.create_table('backend_languagegroup', (
            ('messagegroup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['backend.MessageGroup'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('backend', ['LanguageGroup'])

        # Adding model 'Email'
        db.create_table('backend_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=600)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('backend', ['Email'])

        # Adding model 'AutoTask'
        db.create_table('backend_autotask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal('backend', ['AutoTask'])


    def backwards(self, orm):
        # Deleting model 'AutomatedMessage'
        db.delete_table('backend_automatedmessage')

        # Removing M2M table for field groups on 'AutomatedMessage'
        db.delete_table(db.shorten_name('backend_automatedmessage_groups'))

        # Deleting model 'MessageBase'
        db.delete_table('backend_messagebase')

        # Deleting model 'MessageGroup'
        db.delete_table('backend_messagegroup')

        # Deleting model 'Condition'
        db.delete_table('backend_condition')

        # Deleting model 'StudyGroup'
        db.delete_table('backend_studygroup')

        # Deleting model 'LanguageGroup'
        db.delete_table('backend_languagegroup')

        # Deleting model 'Email'
        db.delete_table('backend_email')

        # Deleting model 'AutoTask'
        db.delete_table('backend_autotask')


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
        'backend.autotask': {
            'Meta': {'object_name': 'AutoTask'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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