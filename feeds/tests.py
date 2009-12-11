"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from datetime import datetime
from rss.models import Feed

class FeedTest(TestCase):
    def setUp(self):
        """
        setup
        """
        #seriously, fixtures here
        user = User.objects.create_user(username="test", email="test@test.com", password="pwtest")
        building = Building.objects.create(owner=user, name="user's default")

        feed = Feed(text="test", feedurl="test.atom", parent=building, last_checked = datetime(2009, 12, 3, 15, 26, 47, 3, 337, 0), score_per_item=10)

    def test_fetch(self):
        new_posts = feed.fetch_new()
        self.assertEquals(3, len(new_posts))
