from functools import partial
from django.views.generic.list_detail import object_list, object_detail
from projx.todo.models import *
from projx.todo.forms import TaskForm
from projx.common.views import access_control, redirect
from django.template import RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render_to_response, get_object_or_404


def all(request):
    #not tested
    tasks = Task.objects.filter(parent__owner=request.user)
    response = partial(object_list, request, queryset=tasks, extra_context={"user": request.user,},  template_name="todo/all.html")
    return access_control(request, request.user, response) #gimped to not actually check the objects: we know they belogn to the user already. But it does the logged-in dance well.

def detail(request, id):
    
    task = get_object_or_404(Task, pk=id)
    response = partial(render_to_response, "todo/task_detail.html", dictionary={"object":task})
    return access_control(request, task.parent.owner, response)

def add_task(request):
    #NOT TESTED
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)

    if request.method == 'POST':
        form = TaskForm( request.POST)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.owner = request.user
            new_object.save()
             #request.user.message_set.create("The %(verbose_name)s was created successfully." % {"verbose_name": "task")
            return HttpResponseRedirect(new_object.get_absolute_url())
    else:
        form = TaskForm()
    # Create the template, context, response
    template_name = "todo/task_form.html"
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    })
    #apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))

def edit_task(request, id):
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)

    if request.method == 'POST':
        task = get_object_or_404(Task, pk=id)
        form = access_control(request, task.parent.owner, partial( TaskForm, request.POST, instance=task))
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.owner = request.user
            new_object.save()
            #  request.user.message_set.create("The %(verbose_name)s was created successfully." % {"verbose_name": "task")
            return HttpResponseRedirect(new_object.get_absolute_url())

    else:
        task = get_object_or_404(Task, pk=id)
        form = access_control(request, task.parent.owner, partial(TaskForm, instance=task)) #booyah! only return the form if we have access perms to the task we're intializing it with.
    # Create the template, context, response
    template_name = "todo/task_form.html"
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    })
    #apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))


#in retrospect, access_control was not a great solution. namely, it doesn't let you call any but one thign at the end. see if we can wrap it on a decorator: can we abstract away get_object_or_404(blah) as well? of course, we coudl wrap mark_done_inner_func in a lambda but, god, no, ugliness and abuse of functional style
def mark_done(request, id):

    def mark_done_inner_func(request, task):
        task.is_done = True
        task.save()
        return redirect("/tasks")

    task = get_object_or_404(Task, pk=id)
    response = partial(mark_done_inner_func, request, task)
    return access_control(request, task.parent.owner, response)


def mark_undone(request, id):

    def mark_undone_inner_func(request, task):
        task.is_done = False
        task.save()
        return redirect("/tasks")

    task = get_object_or_404(Task, pk=id)
    response = partial(mark_undone_inner_func, request, task)
    return access_control(request, task.parent.owner, response)

