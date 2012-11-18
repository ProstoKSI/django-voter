from django.core.exceptions import MiddlewareNotUsed

#from ratings.models import bind_signals

class RatingsMiddleware(object):
    """
    Hack just to call bind_signals after all models loaded
    """
    
    def __init__(self):
        #bind_signals()
        raise MiddlewareNotUsed()

