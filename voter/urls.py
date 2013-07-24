try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url # Django < 1.4

urlpatterns = patterns('voter.views',
    url(r'^like/(?P<obj_type>[\w]+)/(?P<obj_id>[\d]+)/$', 'set_like', name='ratings_like'),
    url(r'^dislike/(?P<obj_type>[\w]+)/(?P<obj_id>[\d]+)/$', 'set_dislike', name='ratings_dislike'),
)

