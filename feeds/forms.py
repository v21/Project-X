from feeds.models import FeedBuilding
from django.forms import *

class FeedBuildingForm(ModelForm):
    class Meta:
        model=FeedBuilding
        fields = ['name', 'feedurl', 'score_per_item']

