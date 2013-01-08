# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from voter.models import VOTE_LIKE, VOTE_DISLIKE

class Migration(DataMigration):

    def forwards(self, orm):
        Book = orm['poetry.book']
        ThreadedComment = orm['threadedcomments.threadedcomment']
        Post = orm['blog.post']
        Profile = orm['auth_ext.profile']
        
        Vote = orm['voter.vote']
        Rating = orm['voter.rating']
        RatingVote = orm['voter.ratingvote']
        
        books = Book.objects.all()
        posts = Post.objects.all()
        comments = ThreadedComment.objects.all()
        profiles = Profile.objects.all()

        def add_rating(obj, model_name):
            vote_list = Vote.objects.filter(object_id=obj.id, content_type__model=model_name)
            if obj.rating == None:
                rating = Rating()
                rating.save()
                obj.rating = rating
                obj.save()
            for vote in vote_list:
                if vote.score > 0:
                    obj.rating.likes += 1
                    vt = VOTE_LIKE
                else:
                    obj.rating.dislikes += 1
                    vt = VOTE_DISLIKE
                rating_vote, is_new = RatingVote.objects.get_or_create(user=vote.user, 
                    rating=obj.rating, vote_type=vt)
                if is_new:
                    rating_vote.save()
            obj.rating.save()

        for book in books:
            add_rating(book, 'book')
        for post in posts:
            add_rating(post, 'post')
        for comment in comments:
            add_rating(comment, 'threadedcomment')
        for profile in profiles:
            add_rating(profile, 'profile')


    def backwards(self, orm):
        pass


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
        'auth_ext.emailconfirmation': {
            'Meta': {'object_name': 'EmailConfirmation'},
            'confirmation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth_ext.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importer_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitation'", 'to': "orm['importer.ImporterInfo']"}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'auth_ext.profile': {
            'Meta': {'object_name': 'Profile'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('thumbnail_works.fields.EnhancedImageField', [], {'max_length': '255', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icq': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '10'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'poetry_font_size': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile_list'", 'null': 'True', 'to': "orm['voter.Rating']"}),
            'sex': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'Europe/Kiev'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'auth_ext.urllogintoken': {
            'Meta': {'object_name': 'UrlLoginToken'},
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'blog.blog': {
            'Meta': {'object_name': 'Blog'},
            'can_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '256', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "'blog_icons/default.jpg'", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'user_access_list': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'blog_user_access_m2m_list'", 'symmetrical': 'False', 'through': "orm['blog.BlogUserAccess']", 'to': "orm['auth.User']"})
        },
        'blog.bloguseraccess': {
            'Meta': {'object_name': 'BlogUserAccess'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blog_user_access_list'", 'to': "orm['blog.Blog']"}),
            'can_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_write': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_moderator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blog_user_access_list'", 'to': "orm['auth.User']"})
        },
        'blog.post': {
            'Meta': {'ordering': "('-updated_at',)", 'object_name': 'Post'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_posts'", 'to': "orm['auth.User']"}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'post_list'", 'null': 'True', 'to': "orm['blog.Blog']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator_ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_comment_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blog_list'", 'null': 'True', 'to': "orm['voter.Rating']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'tease': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'importer.importerinfo': {
            'Meta': {'object_name': 'ImporterInfo'},
            'about': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'poetry.book': {
            'Meta': {'object_name': 'Book'},
            'allow_commercial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_modifications': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'books'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'default_author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'default_books'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'downloads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'finished': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'genre': ('django.db.models.fields.CharField', [], {'default': "'100'", 'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_converted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pages': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_list'", 'null': 'True', 'to': "orm['voter.Rating']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'read_books'", 'blank': 'True', 'through': "orm['poetry.UserReadBook']", 'to': "orm['auth.User']"}),
            'readers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'series_books'", 'null': 'True', 'to': "orm['poetry.BookSeries']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'poetry.bookcontent': {
            'Meta': {'ordering': "['-date']", 'object_name': 'BookContent'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_content'", 'to': "orm['poetry.Book']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'committer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_content_committers'", 'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'\\n\\n'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {})
        },
        'poetry.bookimage': {
            'Meta': {'object_name': 'BookImage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_image_authors'", 'to': "orm['auth.User']"}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_images'", 'to': "orm['poetry.Book']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'poetry.bookseries': {
            'Meta': {'object_name': 'BookSeries'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'poetry.publisherbook': {
            'Meta': {'object_name': 'PublisherBook'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publisher_books'", 'to': "orm['poetry.Book']"}),
            'cover_path': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Publisher'", 'to': "orm['publisher.Publisher']"})
        },
        'poetry.typo': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Typo'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'typo_list'", 'to': "orm['poetry.Book']"}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'poetry.userreadbook': {
            'Meta': {'ordering': "['-id']", 'object_name': 'UserReadBook'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_read_book'", 'to': "orm['poetry.Book']"}),
            'font_size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'read_percent': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'publisher.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'work_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        'voter.rating': {
            'Meta': {'object_name': 'Rating'},
            'dislikes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rating'", 'symmetrical': 'False', 'through': "orm['voter.RatingVote']", 'to': "orm['auth.User']"})
        },
        'voter.ratingvote': {
            'Meta': {'object_name': 'RatingVote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rating_vote_list'", 'to': "orm['voter.Rating']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rating_vote_list'", 'to': "orm['auth.User']"}),
            'vote_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'voter.score': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'Score'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'voter.vote': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'user'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['contenttypes.ContentType']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poller'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'threadedcomments.threadedcomment': {
            'Meta': {'ordering': "('-date_submitted',)", 'object_name': 'ThreadedComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_approved': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'children'", 'null': 'True', 'blank': 'True', 'to': "orm['threadedcomments.ThreadedComment']"}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'threaded_comment_list'", 'null': 'True', 'to': "orm['voter.Rating']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['poetry', 'blog', 'threadedcomments', 'auth_ext', 'voter']
