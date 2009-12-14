"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

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
        feed.last_checked = datetime(2009, 12, 3, 15, 26, 47) #bloody auto_now_add
        feed.save()
        new_posts = feed.fetch_new()
        self.assertEquals(3, len(new_posts))
