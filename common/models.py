from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    slug = models.CharField(max_length=20)


    def __unicode__(self):
        return self.name
        
    def current_score(self):
        scores = Score.objects.filter(parent=self)
        latest_score = scores.order_by("-time")[0]
        return latest_score


class Score(models.Model):
    parent = models.ForeignKey(Building)
    points = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return repr(self.parent) + " had %d points at %s" % (self.points, self.time)

    def __init__(self, *args, **kwargs):
        super(Score, self).__init__(*args, **kwargs)

