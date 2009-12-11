from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    slug = models.CharField(max_length=20)


    def __unicode__(self):
        return self.name
        
    def calc_new_score(self):
        score = Score(parent = self)
        score.save()
        return score.points

    def current_score(self, owner):
        scores = Score.objects.filter(parent=self)
        latest_score = scores.order_by("-time")[0]
        return latest_score.points


class Score(models.Model):
    parent = models.ForeignKey(Building)
    points = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "a score"#self.parent + " had " + self.points + " points at " + self.time

    def __init__(self, *args, **kwargs):
        super(Score, self).__init__(*args, **kwargs)

    def set(self):
        #for performance, this should really be done entirely in sql. but *shrug*
        print "hello?" 
        tasks =  Task.objects.filter(parent=self.parent)
        print tasks 
        cum_score = 0
        for t in tasks:
            if t.is_done:
                cum_score += t.points
        
        self.points = cum_score
       

