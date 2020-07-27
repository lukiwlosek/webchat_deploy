from django.test import TestCase, Client
from django.urls import reverse

from chat.models import Friend, Client, Message
from django.contrib.auth.models import User
from chat_fe.forms import RegistrationForm


class TestViews(TestCase):
    # this is the login test
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        url = reverse("login")
        response = self.client.post(url, self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_active)

