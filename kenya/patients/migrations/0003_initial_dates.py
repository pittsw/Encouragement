# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
		"Write your forwards methods here."
		# Note: Don't use "from appname.models import ModelName". 
		# Use orm.ModelName to refer to models in this application,
		# and orm['appname.ModelName'] for models in other applications.

		#Data Migration
		for client in orm.Client.objects.all():
			msg = orm.Message.objects.filter(client_id=client)
			client_msg = msg.filter(sent_by="Client").order_by('-date')
			system_msg = msg.filter(sent_by="System").order_by('-date')
			client.last_msg_client = None
			client.last_msg_system = None
			if client_msg.count() > 0:
				client.last_msg_client = client_msg[0].date
			if system_msg.count() >0:
				client.last_msg_system = system_msg[0].date
			client.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'backend.automatedmessage': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'AutomatedMessage'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['backend.MessageGroup']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'next_message': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous_message'", 'null': 'True', 'to': "orm['backend.AutomatedMessage']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'send_base': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.MessageBase']", 'null': 'True', 'blank': 'True'}),
            'send_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'backend.condition': {
            'Meta': {'object_name': 'Condition', '_ormbases': ['backend.MessageGroup']},
            'messagegroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['backend.MessageGroup']", 'unique': 'True', 'primary_key': 'True'})
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
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'patients.client': {
            'Meta': {'object_name': 'Client'},
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Condition']"}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'default': "'English'", 'to': "orm['backend.LanguageGroup']"}),
            'last_msg_client': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'last_msg_system': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'living_children': ('django.db.models.fields.IntegerField', [], {}),
            'next_visit': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'partner_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'partner_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pending': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'phone_network': ('django.db.models.fields.CharField', [], {'default': "'safaricom'", 'max_length': '50'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'pregnancy_event': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['patients.PregnancyEvent']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'pregnancy_status': ('django.db.models.fields.CharField', [], {'default': "'Pregnant'", 'max_length': '20'}),
            'previous_pregnacies': ('django.db.models.fields.IntegerField', [], {}),
            'pri_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pri_contact_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'primary_key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship_status': ('django.db.models.fields.CharField', [], {'default': "'Married'", 'max_length': '25'}),
            'sec_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'sec_contact_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'send_day': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'send_time': ('django.db.models.fields.IntegerField', [], {'default': '13'}),
            'signup_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'study_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.StudyGroup']"}),
            'urgent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'years_of_education': ('django.db.models.fields.IntegerField', [], {})
        },
        'patients.interaction': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Interaction'},
            'client_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['patients.Client']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['patients.Nurse']", 'null': 'True', 'blank': 'True'})
        },
        'patients.message': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Message', '_ormbases': ['patients.Interaction']},
            'automated_message': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'automated_message'", 'null': 'True', 'to': "orm['backend.AutomatedMessage']"}),
            'interaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['patients.Interaction']", 'unique': 'True', 'primary_key': 'True'}),
            'prompted': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sent_by': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'patients.note': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Note'},
            'author_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['patients.Nurse']", 'null': 'True', 'blank': 'True'}),
            'client_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['patients.Client']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'patients.nurse': {
            'Meta': {'object_name': 'Nurse'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'patients.phonecall': {
            'Meta': {'ordering': "['-date']", 'object_name': 'PhoneCall', '_ormbases': ['patients.Interaction']},
            'caller': ('django.db.models.fields.CharField', [], {'default': "'nurse'", 'max_length': '10'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'interaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['patients.Interaction']", 'unique': 'True', 'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '10'})
        },
        'patients.pregnancyevent': {
            'Meta': {'object_name': 'PregnancyEvent'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '20'}),
            'outcome': ('django.db.models.fields.CharField', [], {'default': "'live_birth'", 'max_length': '20'})
        },
        'patients.visit': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Visit'},
            'client_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['patients.Client']"}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['patients']
    symmetrical = True
