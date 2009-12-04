from django.db import models
from django.contrib.auth.models import User



class Building(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    slug = models.CharField(max_length=20)


    def __unicode__(self):
        return self.name
    
    def calc_new_score(self, owner=owner):
       pass  
    
    def current(self, owner):
        pass


class Task(models.Model):
    text = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Building)
    slug = models.CharField(max_length=50)
    points = models.IntegerField(default=10)


    def __unicode__(self):
        return self.text

    def get_absolute_url(self):
        return "/tasks/id/%i" % self.id

class Score(models.Model):
    parent = models.ForeignKey(Building)
    points = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "a score"#self.parent + " had " + self.points + " points at " + self.time

    def __init__(self, *args, **kwargs):
        super(Score, self).__init__(*args, **kwargs)


        #for performance, this should really be done entirely in sql. but *shrug*
        
        tasks =  Task.objects.filter(parent=self.parent)
        
        cum_score = 0
        for t in tasks:
            if t.is_done:
                cum_score += t.points
        
        self.points = cum_score
        
