from django.conf.urls import handler404
from django.urls import path

from .import views

urlpatterns = [
    path("login/", views.connexion, name="connexion"),
    path("register/", views.inscription, name="inscription"),
    path("logout/", views.deconnexion, name="deconnexion"),
    path("profile/", views.profile, name="profile"),

    path("", views.index, name="index"),
    path("blog/", views.postList, name="post_list"),
    path("blog/<slug:slug>/", views.postDetail, name="post_detail"),
    path("apropos/", views.apropos, name="apropos"),
    path("contact/", views.contact, name="contact"),
]

