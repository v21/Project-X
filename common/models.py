from django.db import models
from django.contrib.auth.models import User

from django.contrib import admin
from datetime import datetime


#stolen from http://codespatter.com/2009/07/01/django-model-manager-soft-delete-how-to-customize-admin/
class SoftDeleteManager(models.Manager):
    ''' Use this manager to get objects that have a deleted field '''
    def get_query_set(self):
        return super(SoftDeleteManager, self).get_query_set().filter(deleted=False)
    def all_with_deleted(self):
        return super(SoftDeleteManager, self).get_query_set()
    def deleted_set(self):
        return super(SoftDeleteManager, self).get_query_set().filter(deleted=True)
 
class SoftDeleteAdmin(admin.ModelAdmin):
    list_display = ('id', '__unicode__', 'deleted',)
    list_filter = ('deleted',)

class Building(models.Model):
    objects = SoftDeleteManager() #hello, soft deleting
    deleted = models.BooleanField(default=False)

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    slug = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
        
    def current_score(self):
        scores = Score.objects.filter(parent=self)
        try:
            latest_score = scores.order_by("-time", "-points")[0]
        except IndexError: #catching the case where no score's been made yet. TODO
            latest_score = Score(parent = self, points = 0)
        return latest_score

    def create_initial_score(self):
        #create a Score set to 0, so later shit can just check from it...
        score = Score(parent = self, points = 0)
        score.save()
        return score

class Score(models.Model):
    objects = SoftDeleteManager() #hello, soft deleting
    deleted = models.BooleanField(default=False)

    parent = models.ForeignKey(Building)
    points = models.IntegerField()
    time = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ['parent', 'time']

    def __unicode__(self):
        return repr(self.parent) + " had %d points at %s" % (self.points, self.time)

    def __init__(self, *args, **kwargs):
        super(Score, self).__init__(*args, **kwargs)
