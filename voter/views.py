# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from misc.json_encode import json_response
from misc.utils import str_to_class

from voter.models import Rating, RatingVote, VOTE_LIKE, VOTE_DISLIKE
from voter import tasks

RATINGS_CONFIG = getattr(settings, "RATINGS_CONFIG", {})

@login_required
def set_like(request, obj_type, obj_id):
    return set_rating(request, obj_type, obj_id, VOTE_LIKE)

@login_required
def set_dislike(request, obj_type, obj_id):
    return set_rating(request, obj_type, obj_id, VOTE_DISLIKE)

def set_rating(request, obj_type, obj_id, vote_type):
    error = ""
    if obj_type in RATINGS_CONFIG:
        model_name = RATINGS_CONFIG[obj_type]['model']
        model = str_to_class(model_name)
        try:
            obj = model.objects.get(pk=obj_id)
            if obj.rating == None:
                rating = Rating.objects.create()
                rating.save()
                obj.rating = rating
                obj.save()
            vote, is_new = RatingVote.objects.get_or_create(user=request.user, rating=obj.rating)
            if is_new:
                vote.vote_type = vote_type
                vote.save()
                if vote_type == VOTE_LIKE:
                    obj.rating.likes += 1
                else:
                    obj.rating.dislikes += 1
                obj.rating.save()
                tasks.task_compute_object_rating(obj_type, obj)
            else:
                error = _("You already voted")
        except model.DoesNotExist:
            error = _("You can't vote for this object")
    else:
        error = _("You can't vote for this object")
    if request.is_ajax():
        if error:
            return json_response({'status': "error", 'text': error})
        else:
            return json_response({'status': "ok", 
            'text': _("Your vote successfully counted")})
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
