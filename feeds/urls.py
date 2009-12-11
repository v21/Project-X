from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'feeds.views.all'),
)
