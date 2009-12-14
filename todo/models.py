from django.db import models
from django.contrib.auth.models import User
from projx.common.models import Building, Score

class TaskBuilding(Building):
    def set_points(self):
        '''
        Creates a new score, summing up all the completed things. model is the class of the things linked to the building.
        '''
        tasks = Task.objects.filter(parent=self)
        cum_score = 0
        for t in tasks:
            if t.is_done:
                cum_score += t.points
        score = Score(parent=self, points = cum_score)
        score.save()
        return score

class Task(models.Model):
    text = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(TaskBuilding)
    slug = models.CharField(max_length=50)
    points = models.IntegerField(default=10)


    def __unicode__(self):
        return self.text

    def get_absolute_url(self):
        return "/tasks/id/%i" % self.id

