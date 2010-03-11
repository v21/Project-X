from feeds.models import FeedBuilding
from common.views import access_control, google_graph, scores_in_daterange
from common.models import Score
from functools import partial
from django.views.generic.list_detail import object_list, object_detail
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from feeds.forms import FeedBuildingForm
from django.template import RequestContext, loader

'''

what do we need? graphable stuff of scores
the current feed
some overview shit: a generic wi/ feedbuilding data in't

all of this access_control 
'''
def all(request):
    '''
    displays all the user's FeedBuildings.
    '''
    feeds = FeedBuilding.objects.filter(owner__exact=request.user)
    response = partial(object_list, request, queryset=feeds, extra_context={"user": request.user,},  template_name="feeds/all.html")
    return access_control(request, request.user, response) #gimped to not actually check the objects: we know they belogn to the user already. But it does the logged-in dance well.

def detail(request, id):
    '''
    displays detail on a single FeedBuilding
    '''
    fb = get_object_or_404(FeedBuilding, pk=id)
    
    #this is not sustainable. hitting the feed every time soneone updates the page? what if the site goes down? what if... 
    fb.scores_from_new(fb.fetch_new())
    s = scores_in_daterange(fb)
    print s
#    ggraph = google_graph(s)
    response = partial(render_to_response, "feeds/feed_detail.html", dictionary={"object":fb,})# "ggraph":ggraph})
    return access_control(request, fb.owner, response)

def add_feed(request):
    #NOT TESTED
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)

    if request.method == 'POST':
        form = FeedBuildingForm( request.POST)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.owner = request.user
            new_object.save()
             #request.user.message_set.create("The %(verbose_name)s was created successfully." % {"verbose_name": "task")
            return HttpResponseRedirect(new_object.get_absolute_url())
    else:
        form = FeedBuildingForm()
    # Create the template, context, response
    template_name = "feeds/feedbuilding_form.html"
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    })
    #apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))

def edit_feed(request, id):
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)

    if request.method == 'POST':
        fb = get_object_or_404(FeedBuilding, pk=id)
        form = access_control(request, fb.owner, partial( FeedBuildingForm, request.POST, instance=fb))
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.owner = request.user
            new_object.save()
            #  request.user.message_set.create("The %(verbose_name)s was created successfully." % {"verbose_name": "task")
            return HttpResponseRedirect(new_object.get_absolute_url())

    else:
        fb = get_object_or_404(FeedBuilding, pk=id)
        form = access_control(request, fb.owner, partial(FeedBuildingForm, instance=fb)) #booyah! only return the form if we have access perms to the task we're intializing it with.
    # Create the template, context, response
    template_name = "feeds/feedbuilding_form.html"
    t = loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    })
    #apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))

