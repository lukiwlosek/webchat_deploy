from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from chat_fe.views import chat, register, dashboard, change_friends, index, success
from django.contrib.auth.models import User


class TestUrls(TestCase):
    def test_login_url(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_dashboard_url(self):
        url = reverse("dashboard")
        self.assertEquals(resolve(url).func, dashboard)

    def test_room_url(self):
        url = reverse("room", kwargs={"room_name": "4"})
        self.assertEquals(resolve(url).func, chat)

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_change_friends_url(self):
        url = reverse("change_friends", kwargs={"operation": "add", "pk": 4})
        self.assertEquals(resolve(url).func, change_friends)

    def test_index_url(self):
        url = reverse("index", kwargs={"user": "lukasz", "room": "4"})
        self.assertEquals(resolve(url).func, index)

    def test_success_url(self):
        url = reverse("charge", kwargs={"user": "lukasz", "room": "4"})
        self.assertEquals(resolve(url).func, success)
