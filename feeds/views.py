from feeds.models import FeedBuilding
from pygooglechart import XYLineChart 
from common.views import access_control
from common.models import Score
from functools import partial
import time
'''

what do we need? graphable stuff of scores
the current feed
some overview shit: a generic wi/ feedbuilding data in't

all of this access_control 
'''

def google_graph(request,fb_id):
    #missing daterange options...
    #http://docs.djangoproject.com/en/dev/ref/models/querysets/#range is a nice clue

    fb = FeedBuilding.objects.filter(pk=fb_id)[0] #there should be only one...
    scores = Score.objects.filter(parent=fb)
    
    tupled_list = [(score.points, score.time) for score in scores]
    points_list, time_list = zip(*tupled_list) 
    
    epoched_time_list = map(lambda t : int(time.mktime(t.timetuple())), time_list)


    lchart = XYLineChart(500,500)
    lchart.add_data(points_list)
    lchart.add_data(epoched_time_list)

    return lchart
    #return access_control(request, fb.owner, partialled)

def all():
    pass
