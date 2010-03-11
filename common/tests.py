"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from common.models import Building, Score
from common.views import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class scores_in_daterange_Test(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test", email="test@test.com", password="pwtest")
        self.building = Building.objects.create(owner=user, name="user's default")
        user.save()
        self.building.save()
        self.old_score = Score(parent=self.building, points=23, time=datetime(1987, 1, 2, 1, 1, 1))
        self.old_score.save()
        time_yesterday = datetime.now() - timedelta(days=1)
        self.recent_score = Score(parent=self.building, points=42, time=time_yesterday)
        self.recent_score.save()
        time_day_before_yesterday = datetime.now() - timedelta(days=2)
        self.other_recent_score = Score(parent=self.building, points=52, time=time_day_before_yesterday)
        self.other_recent_score.save()

    def test_with_given_daterange(self):
        scores = scores_in_daterange(self.building, (datetime(1987,1,1,0,0,0),datetime(1988,1,1,1,1,1)))
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0], self.old_score)

    def test_with_no_daterange(self):
        scores = scores_in_daterange(self.building)

        self.assertEqual(len(scores), 3)
#        self.assertContains(scores, self.recent_score)
#        self.assertContains(scores, self.other_recent_score)



class scores_in_daterange_with_no_scores_Test(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test", email="test@test.com", password="pwtest")
        self.building = Building.objects.create(owner=user, name="user's default")
        user.save()
        self.building.save()


    def test_with_given_daterange(self):
        scores = scores_in_daterange(self.building, (datetime(1987,1,1,0,0,0),datetime(1988,1,1,1,1,1)))
        self.assertEqual(len(scores), 0)

    def test_with_no_daterange(self):
        scores = scores_in_daterange(self.building)
        self.assertEqual(len(scores), 1)
