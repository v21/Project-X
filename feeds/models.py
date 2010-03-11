from django.db import models
from projx.common.models import Building, Score
from datetime import datetime
import feedparser
import time
from itertools import groupby


class FeedBuilding(Building):
    feedurl = models.CharField(max_length=255)
    last_checked = models.DateTimeField(default=datetime.now())
    score_per_item = models.IntegerField(default=10) #do we need a more complex representaton?
    def save(self, *args, **kwargs):
        super(FeedBuilding, self).save(*args, **kwargs)
        if not self.id:
            self.create_initial_score()
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/feeds/id/%i" % self.id

    def fetch_new(self):

        feed = feedparser.parse(self.feedurl)
        new_items= []
        for e in feed.entries:
            try:
                feed_timestamp = e.published_parsed[:6]
            except AttributeError: #unless it doesn't have that.
                try:
                    feed_timestamp = e.updated_parsed[:6]
                except AttributeError: #or that: we buggered.
                    break 

            if datetime(*feed_timestamp) > self.last_checked: #this triggers when there's new items. it adds a new score.
                e.timestamp = feed_timestamp
                new_items += [e]

        self.last_checked = datetime(*feed_timestamp)
        self.save()

        return new_items

    def scores_from_new(self, new_items):
        new_items.sort(key = lambda i : i.timestamp)
        items_by_timestamp = [list(g) for k,g in groupby(new_items, key = lambda i: i.timestamp)] #whew! so this converts new_items into a list that contains lists of simultaneous events

        scores = []
        for event in items_by_timestamp:
            points = self.current_score().points
            for item in event:
                points += self.score_per_item
            score = Score(points = points, parent = self, time = datetime(*event[0].timestamp))
            score.save()
            scores += [score]
        return scores

'''
a list which we want to convert into a list of Scores

any simultaneous entries wanna be summed, done as a single score.

and the non-simulatenous get their own Scores.

so first: a list of lists. each list contains all the new_items that happen at any one time.


'''


'''
            if datetime(*feed_timestamp) == self.last_checked: #this checks to see whether this update is made at exactly the same time as the last update. in which case it's one big bonanza update - update the score with the new points instead.
                try:
                    score = Score.objects.filter(time=self.last_checked)[0]
                    score.points += self.score_per_item
                    score.save()
                except IndexError:
                    pass #TODO denormalization has gone wrong. dogs are fornicating with cats. self.current_score().time differs from self.last_checked



                new_points = self.score_per_item + self.current_score().points
                score = Score(points = new_points, parent = self)
                score.save()
                score.time = datetime(*feed_timestamp)
                score.save()
'''
