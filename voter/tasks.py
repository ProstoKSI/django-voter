from django.conf import settings

from misc.utils import str_to_class


def task_compute_object_rating(obj_type, obj):
    return str_to_class(settings.RATINGS_CONFIG[obj_type]['compute_func']).delay(obj.id)
