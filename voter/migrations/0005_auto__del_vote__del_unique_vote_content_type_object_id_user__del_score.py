# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Score', fields ['content_type', 'object_id']
        db.delete_unique('ratings_score', ['content_type_id', 'object_id'])

        # Removing unique constraint on 'Vote', fields ['content_type', 'object_id', 'user']
        db.delete_unique('ratings_vote', ['content_type_id', 'object_id', 'user_id'])

        # Deleting model 'Vote'
        db.delete_table('ratings_vote')

        # Deleting model 'Score'
        db.delete_table('ratings_score')

        # Adding model 'Badge'
        db.create_table('ratings_badge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rating_weight', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('ratings', ['Badge'])

        # Adding M2M table for field users on 'Badge'
        db.create_table('ratings_badge_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('badge', models.ForeignKey(orm['ratings.badge'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('ratings_badge_users', ['badge_id', 'user_id'])


    def backwards(self, orm):
        
        # Adding model 'Vote'
        db.create_table('ratings_vote', (
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='poller', null=True, to=orm['auth.User'], blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['contenttypes.ContentType'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ratings', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['content_type', 'object_id', 'user']
        db.create_unique('ratings_vote', ['content_type_id', 'object_id', 'user_id'])

        # Adding model 'Score'
        db.create_table('ratings_score', (
            ('votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ratings', ['Score'])

        # Adding unique constraint on 'Score', fields ['content_type', 'object_id']
        db.create_unique('ratings_score', ['content_type_id', 'object_id'])

        # Deleting model 'Badge'
        db.delete_table('ratings_badge')

        # Removing M2M table for field users on 'Badge'
        db.delete_table('ratings_badge_users')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ratings.badge': {
            'Meta': {'object_name': 'Badge'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rating_weight': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'badge_list'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ratings.rating': {
            'Meta': {'object_name': 'Rating'},
            'dislikes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rating'", 'symmetrical': 'False', 'through': "orm['ratings.RatingVote']", 'to': "orm['auth.User']"})
        },
        'ratings.ratingvote': {
            'Meta': {'object_name': 'RatingVote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rating_vote_list'", 'to': "orm['ratings.Rating']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rating_vote_list'", 'to': "orm['auth.User']"}),
            'vote_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['ratings']