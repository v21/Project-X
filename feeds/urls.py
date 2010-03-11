from django.conf.urls.defaults import *

urlpatterns = patterns('feeds.views',
    (r'^$', 'all'),
    (r'^id/(\d+)$', 'detail'),
    (r'^add', 'add_feed'),
    (r'^edit/(\d+)$', 'edit_feed'),
)
