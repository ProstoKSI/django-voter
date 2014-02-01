try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from misc.utils import str_to_class


def recompute_obj_ratings(model, compute_func):
    print("Computing ratings for %s" % str(model))
    if model != User:
        obj_list = model.objects.filter(Q(rating__likes__gte=1) | Q(rating__dislikes__gte=1))
    else:
        obj_list = model.objects.all()
    for i, obj_id in enumerate(obj_list.values_list('id', flat=True)):
        compute_func(obj_id, is_event=False)
        if i % 100 == 0:
            print("\t%d done." % i)

def recompute_ratings(obj_type='all'):
    if obj_type == 'all':
        recompute_objs = ((rating_config['model'], rating_config['compute_func'])
            for rating_config in settings.RATINGS_CONFIG.itervalues())
    elif obj_type in settings.RATINGS_CONFIG:
        rating_config = settings.RATINGS_CONFIG[obj_type]
        recompute_objs = (rating_config['model'], rating_config['compute_func'])
    else:
        recompute_objs = ()
    for model, compute_func in recompute_objs:
        recompute_obj_ratings(str_to_class(model), str_to_class(compute_func))
