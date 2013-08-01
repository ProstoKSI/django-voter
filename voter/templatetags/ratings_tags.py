# -*- coding: utf-8 -*-
from django.template import Node, Variable, TemplateSyntaxError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

if 'coffin' in settings.INSTALLED_APPS:
    from coffin.template import Library
else:
    from django.template import Library

try:
    # Rating widgets don't depend on other templates, so it's safe to use quite
    # more fast rendering by jinja2 instead of django's.
    # In our project we achive 10ms instead of 400ms rendering time on 10 (ten)
    # renderings ({% render_rating %}).
    from coffin.shortcuts import render_to_string
except ImportError:
    from django.template.loader import render_to_string

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from voter.models import Rating, RatingVote

register = Library()

if 'coffin' in settings.INSTALLED_APPS:
    register.simple_tag = register.object

RATINGS_CONFIG = getattr(settings, "RATINGS_CONFIG", {})
RATING_TABLE_COUNT = getattr(settings, 'RATING_TABLE_COUNT', 5)


@register.simple_tag
def get_rating(obj):
    rating = '%.1f' % obj.rating_score
    if obj.rating_score > 0:
        rating = '+' + rating
        rating_class = "positive"
    elif obj.rating_score < 0:
        rating_class = "negative"
    else:
        rating_class = "default"
    return rating, rating_class

@register.inclusion_tag('voter/user_rating.html', takes_context=True)
def get_user_rating_div(context, obj):
    context['rating'] = get_rating(obj)
    return context

@register.simple_tag
def can_vote(current_user, owner, rating):
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
       
    def render(self, context, template_name="voter/default_rating.html"):
        obj = self.obj.resolve(context)
        obj_type = self.obj_type.resolve(context)
        if self.user: 
            user = self.user.resolve(context)
        else:
            user = None
        rating, rating_class = get_rating(obj)
        context['rating'] = rating
        context['can_vote'] = can_vote(context['request'].user, user, obj.rating)
        context['rating_class'] = rating_class
        context['obj_id'] = obj.id
        context['obj_type'] = obj_type
        
        return render_to_string(template_name, context)

@register.simple_tag
def get_top_users():
    return User.objects.order_by('-rating_score')[:RATING_TABLE_COUNT]

@register.simple_tag
def get_top_books():
    from poetry.models import Book
    return Book.objects.order_by('-rating_score')[:RATING_TABLE_COUNT]

@register.inclusion_tag('voter/rating_table.html', takes_context=True)
def get_rating_table(context):
    context['top_users'] = get_top_users()
    context['top_books'] = get_top_books()
    return context

