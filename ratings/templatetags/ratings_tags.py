# -*- coding: utf-8 -*-
from django import template
from django.template import Node, Variable, TemplateSyntaxError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template, select_template
from django.contrib.auth.models import User

from ratings.models import Rating, RatingVote

register = template.Library()

RATINGS_CONFIG = getattr(settings, "RATINGS_CONFIG", {})
RATING_TABLE_COUNT = getattr(settings, 'RATING_TABLE_COUNT', 5)

@register.simple_tag
def get_rating_span(obj):
    rating = str(obj.rating_score)
    if score > 0:
        rating += '+'
        rating_class = "positive"
    elif score < 0:
        rating_class = "negative"
    else:
        rating_class = "default"
    return "<span class=\"" + rating_class + "\">" + rating + "</span>"

@register.inclusion_tag('ratings/user_rating.html', takes_context=True)
def get_user_rating_div(context, obj):
    rating = round(obj.rating_score, 1)
    if abs(rating) < 2210:
        context['score'] = abs(int(rating/23))
    else:
        context['score'] = 96
    context['rating'] = rating
    return context
    
@register.tag
def render_rating(parser, token):
    bits = token.contents.split(' ')[1:]
    if not (len(bits) == 2 or len(bits) == 3):
        raise TemplateSyntaxError("Incorrect count of parameters %d expected 2 or 3" % len(bits))
    if len(bits) == 2:
        return RenderRatingNode(bits[0], bits[1])
    else:
        return RenderRatingNode(bits[0], bits[1], bits[2])
    
class RenderRatingNode(Node):
    
    def __init__(self, obj, obj_type, user=None):
        self.obj = Variable(obj)
        self.obj_type = Variable(obj_type)
        self.user = user and Variable(user) or None

    def can_vote(self, current_user, owner, rating):
        # Check if anonymus
        res = current_user.is_authenticated()
        # Check if this object owned by current user
        if res and owner:    
            # Check, if owner is list, turple, or some other iterable object - to check on all items of it
            if getattr(owner, '__iter__', False):
                res = reduce(lambda r, u: r and u != current_user, owner, True)
            else:
                res = owner != current_user
        # Check if already voted
        if res:
            res = not RatingVote.objects.filter(rating=rating, user=current_user).exists()
        return res

    def get_rating(self, obj):
        rating = '%.1f' % obj.rating_score
        if obj.rating_score > 0:
            rating = '+' + rating
            rating_class = "positive"
        elif obj.rating_score < 0:
            rating_class = "negative"
        else:
            rating_class = "default"
        return rating, rating_class
        
    def render(self, context, template_name="ratings/default_rating.html"):
        obj = self.obj.resolve(context)
        obj_type = self.obj_type.resolve(context)
        if self.user: 
            user = self.user.resolve(context)
        else:
            user = None
        can_vote = self.can_vote(context['request'].user, user, obj.rating)
        rating, rating_class = self.get_rating(obj)
        context['rating'] = rating
        context['can_vote'] = can_vote
        context['rating_class'] = rating_class
        context['obj_id'] = obj.id
        context['obj_type'] = obj_type
        
        t = get_template(template_name)
        return t.nodelist.render(context)


@register.inclusion_tag('ratings/rating_table.html', takes_context=True)
def get_rating_table(context):
    from poetry.models import Book
    context['top_users'] = User.objects\
        .order_by('-profile__rating_score')[:RATING_TABLE_COUNT]
    context['top_books'] = Book.objects\
        .order_by('-rating_score')[:RATING_TABLE_COUNT]
    return context

