from django.db import models
from projx.common.models import Building, Score
from datetime import datetime
import feedparser
import time

class FeedBuilding(Building):
    feedurl = models.CharField(max_length=255)
    last_checked = models.DateTimeField(auto_now_add=True)
    score_per_item = models.IntegerField(default=10) #do we need a more complex representaton?
    
    def __unicode__(self):
        return self.name

    def fetch_new(self):

        feed = feedparser.parse(self.feedurl)
        new_items= []
        for e in feed.entries:
            if datetime(*e.published_parsed[:6]) > self.last_checked:
                new_items += [e]
            else:
                pass #break #cuz theyre chronological, we can do this. yes?
        
        new_points = self.score_per_item * len(new_items) + self.current_score().points
        score = Score(points = new_points, parent = self)
        score.save()
        last_checked = datetime.now()
        return new_items

    def __init__(self, *args, **kwargs):
        super(FeedBuilding, self).__init__(*args, **kwargs)

