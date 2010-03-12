from django.contrib.auth.views import redirect_to_login
from django.template import RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.dateformat import format as human_date
from django.core import urlresolvers
import pygooglechart

from models import Score
import time, datetime

def redirect(to, *args, **kwargs):
    """
    backported from 1.1 django.shortcuts
    Returns an HttpResponseRedirect to the apropriate URL for the arguments
    passed.
    
    The arguments could be:
    
        * A model: the model's `get_absolute_url()` function will be called.
    
        * A view name, possibly with arguments: `urlresolvers.reverse()` will
          be used to reverse-resolve the name.
         
        * A URL, which will be used as-is for the redirect location.
        
    By default issues a temporary redirect; pass permanent=True to issue a
    permanent redirect
    """
    if kwargs.pop('permanent', False):
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect
    
    # If it's a model, use get_absolute_url()
    if hasattr(to, 'get_absolute_url'):
        return redirect_class(to.get_absolute_url())
    
    # Next try a reverse URL resolution.
    try:
        return redirect_class(urlresolvers.reverse(to, args=args, kwargs=kwargs))
    except urlresolvers.NoReverseMatch:
        # If this is a callable, re-raise.
        if callable(to):
            raise
        # If this doesn't "feel" like a URL, re-raise.
        if '/' not in to and '.' not in to:
            raise
        
    # Finally, fall back and assume it's a URL
    return redirect_class(to)


def access_control(request, owner, callback):
    '''
    This factors out the "is this user allowed to look at this object" code. 
    It would be much neater as a decorator, but sadly we need to pick the object first.
    To use it: use functools.partial, to freeze the view you want called if the user 
    does have permission (like so:  access_control(request, owner, partial(func, arg1, arg2, argn)) )
    Lazy evaluation ftw!
    '''
    if request.user.is_authenticated():
        if request.user.is_active:
            if owner == request.user:
                return callback()
            else:
                raise Http404 #replace with "not authed" page
        else:
            raise Http404 #replace with "not authed" page?
    else:
        return redirect_to_login(request.path)


def scores_in_daterange(building, daterange=None):
    """
    returns a list of scores that occured for a building within a given daterange
    without startdate and enddate it defaults to showing the last week
    """
    if daterange == None:
        daterange = (datetime.datetime.today() - datetime.timedelta(weeks=1), datetime.datetime.today() + datetime.timedelta(days=1)) #i thought __range was inclusive, not exclusive
    scores = list(Score.objects.filter(parent=building).filter(time__range = daterange))
    if daterange[1] >= datetime.datetime.today(): #if the chart goes up to today, incluse an extra point at the current time, with current_score
        scores.append(building.current_score())

    return scores

def google_graph(scores, dim_x=600, dim_y=400):
    '''
    returns a google chart api url for a png graph of the scores for building. chart has dimensions dim_x by dim_y
    '''
    if len(scores) < 2: #scores has to have at least two values to be graphed nicely.
        raise ValueError

    tupled_list = [(score.points, score.time) for score in scores]

    try:
        points_list, time_list = zip(*tupled_list) 
    except ValueError: #catching there being nothing matching
        return None

    epoched_time_list = map(lambda t : int(time.mktime(t.timetuple())), time_list)

    #to be clear here: time is x, points is y

    x_min = min(epoched_time_list)
    x_max = max(epoched_time_list)

    #plus a little padding
    x_diff = x_max - x_min
    x_max += x_diff/20

    y_min = min(min(points_list), 0)
    y_max = max(points_list) + 10

    #plus a little padding
    y_diff = y_max - y_min
    y_max += y_diff/20


    lchart = pygooglechart.XYLineChart(dim_x, dim_y, x_range = [x_min, x_max], y_range=[y_min, y_max])
    lchart.add_data(epoched_time_list)
    lchart.add_data(points_list)

    lchart.set_axis_range(pygooglechart.Axis.LEFT, y_min, y_max)

    
    date_format = 'n/j/y P' #this isn't the prettiest it could be...
    try:
        x_labels = [human_date(datetime.datetime.utcfromtimestamp(d), date_format) for d in range(x_min, x_max, x_diff/5)]
    except ValueError: #breaks on only one score
        x_labels = human_date(datetime.datetime.utcfromtimestamp(x_min), date_format)
    
    lchart.set_axis_labels(pygooglechart.Axis.BOTTOM, x_labels)

    return lchart.get_url()
    

