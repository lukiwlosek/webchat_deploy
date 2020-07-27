from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("register/", views.register, name="register"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
    path("chat/", views.dashboard, name="dashboard"),
    path("chat/<str:room_name>/", views.chat, name="room"),
    path("chat/<operation>/<pk>/", views.change_friends, name="change_friends"),
    path("index/<user>/<room>/", views.index, name="index"),
    path("charge/<user>/<room>/", views.success, name="charge"),
]

