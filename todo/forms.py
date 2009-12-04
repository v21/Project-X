from todo.models import Task
from django.forms import *

class TaskForm(ModelForm):
    class Meta:
        model=Task
        fields = ['text', 'desc', 'due_date', 'points']
