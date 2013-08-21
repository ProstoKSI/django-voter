from math import log, pow

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Max
from voter.models import Rating, Badge, RatingVote, VOTE_LIKE, VOTE_DISLIKE

from poetry.models import Book
from blog.models import Post
from threadedcomments.models import ThreadedComment
from feeds.models import FollowItem
from feeds.views import get_object_type_id

DEFAULT_RATING_WEIGHT = 1
DEFAULT_RATING_BONUS = 0

def get_user_badge(user):
    badge_list = user.badge_list.all().aggregate(
        rating_weight=Max('rating_weight'),
        rating_bonus=Max('rating_bonus')
    )
    if badge_list['rating_weight'] is not None:
        return badge_list
    return {
        'rating_weight': DEFAULT_RATING_WEIGHT, 
        'rating_bonus': DEFAULT_RATING_BONUS,
    }

def get_weighted_vote(rating):
    score = 0
    vote_list = RatingVote.objects.filter(rating=rating)
    for vote in vote_list:
        badge = get_user_badge(vote.user)
        score += (+1 if vote.vote_type == VOTE_LIKE else -1) * badge['rating_weight']
    return score

def compute_book_rating(book):
    book.rating.score = get_weighted_vote(book.rating)
    book.rating.save()
    book.rating_score = book.rating.score
    book.save()

def compute_post_rating(post):
    post.rating.score = post.rating.likes - post.rating.dislikes
    post.rating.save()
    post.rating_score = post.rating.score
    post.save()

def compute_comment_rating(comment):
    comment.rating.score = comment.rating.likes - comment.rating.dislikes
    comment.rating.save()
    comment.rating_score = comment.rating.score
    comment.save()

def get_followers_count(user):
    obj_type, obj_id = get_object_type_id(user)
    count = FollowItem.objects.filter(content_type=obj_type, object_id=obj_id).count()
    return count

def compute_user_rating(user):
    score = 0
    book_list = Book.objects.filter(authors=user)
    book_score = 0
    for book in book_list:
        if book.size > 0:
            book_score += get_weighted_vote(book.rating) * log(book.size * 1.0 / 10 + 1.0) / 2
    post_list = Post.objects.filter(author=user)
    post_score = 0
    for post in post_list:
        post_score += post.rating_score
    book_and_post_score = (book_score * 5 + post_score) * 15

    followers_score = log(get_followers_count(user) + 1.0)
    if book_and_post_score != 0:
        score = book_and_post_score / pow(abs(book_and_post_score), 1.0/3) + followers_score
        score /= 3

    badge = get_user_badge(user)
    score += badge['rating_bonus']

    user.rating.score = score
    user.rating.save()
    user.rating_score = user.profile.rating.score
    user.save()

def recompute_obj_ratings(model, func):
    print("Computing ratings for %s" % str(model))
    if model != User:
        obj_list = model.objects.filter(Q(rating__likes__gte=1) | Q(rating__dislikes__gte=1))
    else:
        obj_list = model.objects.all()
    for i, obj in enumerate(obj_list):
        func(obj)
        if i % 100 == 0:
            print("\t%d done." % i)

def recompute_ratings(obj_type='all'):
    if obj_type in ('book', 'all'):
        recompute_obj_ratings(Book, compute_book_rating)
    if obj_type in ('post', 'all'):
        recompute_obj_ratings(Post, compute_post_rating)
    if obj_type in ('comment', 'all'):
        recompute_obj_ratings(ThreadedComment, compute_comment_rating)
    if obj_type in ('user', 'all'):
        recompute_obj_ratings(User, compute_user_rating)

