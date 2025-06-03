from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect


def custom_logout(request):
    logout(request)
    return redirect("seasons")


urlpatterns = [
    path("", views.seasons, name="seasons"),
    path("seasons", views.seasons, name="seasons"),
    path("season/<int:id>", views.season, name="season"),
    path("episodes", views.episodes, name="episodes"),
    path("episode/<int:id>", views.episode, name="episode"),
    path("episode/prev/<int:id>", views.prev_episode, name="prev_episode"),
    path("episode/next/<int:id>", views.next_episode, name="next_episode"),
    path("casts", views.casts, name="casts"),
    path("episode/<int:id>/like/", views.like_episode, name="like_episode"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", custom_logout, name="logout"),
]
