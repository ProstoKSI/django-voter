try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.db.models import Q

def recompute_obj_ratings(model, compute_func):
    print("Computing ratings for %s" % str(model))
    if model != User:
        obj_list = model.objects.filter(Q(rating__likes__gte=1) | Q(rating__dislikes__gte=1))
    else:
        obj_list = model.objects.all()
    for i, obj in enumerate(obj_list):
        compute_func(obj, is_event=False)
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
