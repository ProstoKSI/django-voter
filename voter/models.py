import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from misc.decorators import receiver

VOTE_LIKE, VOTE_DISLIKE = range(2)

VOTE_CHOICES = (
    (VOTE_LIKE, _("Like")),
    (VOTE_DISLIKE, _("Dislike"))
)

class RatingVote(models.Model):
    user = models.ForeignKey(User, related_name="rating_vote_list")
    rating = models.ForeignKey('Rating', related_name="rating_vote_list")
    vote_type = models.IntegerField("Vote type", choices=VOTE_CHOICES, 
        default=VOTE_LIKE)
    date = models.DateTimeField("Date", auto_now_add=True)


class Rating(models.Model):
    score = models.FloatField(_("Score"), default=0)
    likes = models.IntegerField(_("Likes"), default=0)
    dislikes = models.IntegerField(_("Dislikes"), default=0)
    users = models.ManyToManyField(User, through=RatingVote, verbose_name=_("Users"), related_name="rating")

    def get_objects_name(self):
        try:
            profile = self.profile_list
            return "User: %s" % profile.user.username
        except ObjectDoesNotExist:
            pass
        try:
            book = self.book_list
            return "Book: \"%s\", author: %s" % (book.name, book.default_author.username)
        except ObjectDoesNotExist:
            pass
        try:
            post = self.post_list
            return "Post: \"%s\", author: %s" % (post.title, post.author.username)
        except ObjectDoesNotExist:
            pass
        try:
            comment = self.comment_list
            return "Comment: \"%s\", author %s" % (comment.comment[:50], comment.user.username)
        except ObjectDoesNotExist:
            pass
        return "<No info>"
 

class Badge(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    description = models.CharField(_("Description"), max_length=255)
    visible = models.BooleanField(_("Visible"), default=False)
    rating_weight = models.FloatField(_("Rating weight"), default=0)
    rating_bonus = models.FloatField(_("Rating bonus"), default=0)
    users = models.ManyToManyField(User, verbose_name=_("Users"), related_name="badge_list")


def create_rating():
    return Rating.objects.create()

def RatingField(related_name):
    return models.OneToOneField(Rating, verbose_name=_("Rating"), related_name=related_name)

