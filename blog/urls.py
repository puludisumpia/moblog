from django.urls import path

from .import views

urlpatterns = [
    path("login/", views.connexion, name="connexion"),
    path("register/", views.inscription, name="inscription"),
    path("logout/", views.deconnexion, name="deconnexion"),
    path("", views.index, name="index"),
    path("blog/", views.post_list, name="post_list"),
    path("blog/<slug:slug>/", views.post_detail, name="post_detail"),
    path("apropos/", views.apropos, name="apropos"),
    path("contact/", views.contact, name="contact"),
]
