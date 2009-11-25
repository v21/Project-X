"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from todo.views import *
from todo.models import Task
from django.contrib.auth.models import User
import datetime


class TaskViews(TestCase):
    def setUp(self):
        #this shit needs to get shunted fixture-wards
        user = User.objects.create_user(username="test", email="test@test.com", password="pwtest")
        Task.objects.create(owner=user, text="Sample Task", desc="Sample Description")
        user_denied = User.objects.create_user(username="testdenied", email= "testt@otherurl.com", password="blah")
        user_inactive = User.objects.create_user(username="testinactive",email="bullcrap@whydoineedtoenterthis.com", password="test")
        user_other = User.objects.create_user(username="testother", email="test@test.com", password="pwtest")
        Task.objects.create(owner=user_other, text="French Green Frogs", desc="MORE TEA VICAR", is_done = True)
        Task.objects.create(owner=user_other, text="EDIT ME", desc="YES EDIT EDIT EDIT")

        
    def test_task_index_notloggedin(self):
        response = self.client.get("/tasks/")
        self.assertEquals(response.status_code, 302)

    def test_access_allowed(self):
        c = Client()
        c.login(username="test", password="pwtest")
        response = c.get("/tasks/id/1")
        self.assertEquals(response.status_code, 200)
   

    def test_access_denied(self):
        c = Client()
        c.login(username="testdenied", password="blah")
        response = c.get("/tasks/id/1")
        self.assertEquals(response.status_code, 404)

    def test_inactive_denied(self):
        self.client.login(username="testinactive", password="test")
        response = self.client.get("/tasks/id/1")
        self.assertEquals(response.status_code, 404)

    def test_not_logged_in(self):
        response = self.client.get("/tasks/id/1")
        self.assertEquals(response.status_code, 302)
        

    def test_missing(self):
        self.client.login(username="test", password="pwtest")
        response = self.client.get("/tasks/id/9823740")
        self.assertEquals(response.status_code, 404)

    def test_first_task_correct(self):
        self.client.login(username="test", password="pwtest")
        response = self.client.get("/tasks/id/1")
        self.assertContains(response, "Sample Task", status_code=200)

    def test_second_task_correct(self):
        self.client.login(username="testother", password="pwtest")
        response = self.client.get("/tasks/id/2")
        self.assertContains(response, "French Green Frogs", status_code=200)
        
    def test_mark_done(self):
        self.client.login(username="test", password="pwtest")
        self.assertEquals(Task.objects.get(pk=1).is_done, False)
        response = self.client.get("/tasks/mark_done/1")
        self.assertContains(response,"", status_code=302)
        self.assertEquals(Task.objects.get(pk=1).is_done, True)
    
    def test_mark_done_unauthed(self):
        self.client.login(username="testother", password="pwtest")
        self.assertEquals(Task.objects.get(pk=1).is_done, False)
        response = self.client.get("/tasks/mark_done/1")
        self.assertEquals(response.status_code,404)
        self.assertEquals(Task.objects.get(pk=1).is_done, False)
    
   

    def test_mark_undone(self):
        self.client.login(username="testother", password="pwtest")
        self.assertEquals(Task.objects.get(pk=2).is_done, True)
        response = self.client.get("/tasks/mark_undone/2")
        self.assertContains(response,"", status_code=302)
        self.assertEquals(Task.objects.get(pk=2).is_done, False)

    def test_mark_undone_unauthed(self):
        self.client.login(username="test", password="pwtest")
        self.assertEquals(Task.objects.get(pk=2).is_done, True)
        response = self.client.get("/tasks/mark_undone/2")
        self.assertEquals(response.status_code,404)
        self.assertEquals(Task.objects.get(pk=2).is_done, True)
   
    def test_edit_authed(self):
        self.client.login(username="testother", password="pwtest")
        response = self.client.get("/tasks/id/3")
        self.assertContains(response, "EDIT ME", status_code=200)
        response = self.client.post("/tasks/edit/3", {"text":"EDITED","desc":"YES"})
        self.assertEquals(Task.objects.get(pk=3).text, "EDITED")

    def test_edit_unauthed(self):
        response = self.client.get("/tasks/id/3")
        self.assertEquals(response.status_code,302)
        response = self.client.post("/tasks/edit/3", {"id_text":"EDITED",})
        self.assertEquals(response.status_code,302)

    def test_edit_wrongauthed(self):
        self.client.login(username="test", password="pwtest")
        response = self.client.get("/tasks/id/3")
        self.assertEquals(response.status_code,404)
        response = self.client.post("/tasks/edit/3", {"id_text":"EDITED",})
        self.assertEquals(response.status_code,404)

        
