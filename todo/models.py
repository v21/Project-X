from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    text = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    slug = models.CharField(max_length=50)
    points = models.IntegerField(default=10)


    def __unicode__(self):
        return self.text

    def get_absolute_url(self):
        return "/tasks/id/%i" % self.id
