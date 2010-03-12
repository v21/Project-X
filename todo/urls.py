from django.conf.urls.defaults import *

urlpatterns = patterns('projx.todo.views',
    (r'^$', 'all'),
    (r'^id/(\d+)$', 'detail'),
    (r'^add', 'add_task'),
    (r'^edit/(\d+)$', 'edit_task'),
    (r'^mark_done/(\d+)$', 'mark_done'),
    (r'^mark_undone/(\d+)$', 'mark_undone'),

)
