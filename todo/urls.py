from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'todo.views.all'),
    (r'^id/(\d+)$', 'todo.views.detail'),
    (r'^add', 'todo.views.add_task'),
    (r'^edit/(\d+)$', 'todo.views.edit_task'),
    (r'^mark_done/(\d+)$', 'todo.views.mark_done'),
    (r'^mark_undone/(\d+)$', 'todo.views.mark_undone'),

)
