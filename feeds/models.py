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
        return self.text

    def fetch_new(self):

        feed = feedparser.parse(self.feedurl)
        new_feeds = []
        for e in feed.entries:
            if datetime(*e.published_parsed[:6]) > self.last_checked:
                new_feeds += [e]
            else:
                pass #break #cuz theyre chronological, we can do this. yes?

        last_checked = datetime.now()
        return new_feeds
        
    def __init__(self, *args, **kwargs):
        super(FeedBuilding, self).__init__(*args, **kwargs)
        self.fetch_new()

