from django.db import models
from projx.common import Building, Score
from datetime import datetime

class Feed(models.Model):
    text = models.CharField(max_length=100)
    feedurl = models.CharField(max_length=255)
    parent = models.ForeignKey(Building)
    last_checked = models.DateTimeField(auto_now_add=True)
    score_per_item = models.IntegerField() #do we need a more complex representaton?
    
    def __unicode__(self):
        return self.text

    def fetch_new(self):

        feed = feedparser.parse(self.feedurl)
        new_feeds = []

        for e in feed.entries:
            if e.published_parsed > self.last_checked:
                new_feeds += e
            else:
                break #cuz theyre chronological, we can do this. yes?

        last_checked = datetime.now()
        return new_feeds



