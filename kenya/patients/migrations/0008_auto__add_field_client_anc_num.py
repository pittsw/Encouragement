# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Client.anc_num'
        db.add_column('patients_client', 'anc_num',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Client.anc_num'
        db.delete_column('patients_client', 'anc_num')


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
        'backend.condition': {
            'Meta': {'object_name': 'Condition', '_ormbases': ['backend.MessageGroup']},
            'messagegroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['backend.MessageGroup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'backend.languagegroup': {
            'Meta': {'object_name': 'LanguageGroup', '_ormbases': ['backend.MessageGroup']},
            'messagegroup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['backend.MessageGroup']", 'unique': 'True', 'primary_key': 'True'})
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
            'anc_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'pregnancy_status': ('django.db.models.fields.CharField', [], {'default': "'Pregnant'", 'max_length': '20'}),
            'previous_pregnacies': ('django.db.models.fields.IntegerField', [], {}),
            'pri_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pri_contact_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'primary_key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship_status': ('django.db.models.fields.CharField', [], {'default': "'Married'", 'max_length': '25'}),
            'repeat_msg': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'client': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['patients.Client']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scheduled_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['patients']