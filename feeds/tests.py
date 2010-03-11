from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime
from feeds.models import FeedBuilding
from projx.common.models import Building, Score


class FeedModels(TestCase):
    def setUp(self):
        """
        setup
        """
        #seriously, fixtures here

    def test_fetch(self):
        user = User.objects.create_user(username="test", email="test@test.com", password="pwtest")
        user.save()
        feed = FeedBuilding(name="test",owner=user, feedurl="/home/v21/projx/feeds/test.atom", last_checked=datetime(2009, 12, 3, 15, 26, 47), score_per_item=10)
        feed.save()
        new_posts = feed.fetch_new()
        self.assertEquals(3, len(new_posts))
        feed.scores_from_new(new_posts)
        self.assertEquals(30, feed.current_score().points)

    """
    from common.models import Score
    from django.contrib.auth.models import User
    from feeds.models import FeedBuilding
    me = User.objects.all()[0]
    fb = FeedBuilding(feedurl="http://github.com/v21.atom", score_per_item=10,owner = me, name="Github")
    fb.fetch_new()
    """
