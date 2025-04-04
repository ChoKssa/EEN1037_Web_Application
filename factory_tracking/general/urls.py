from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("submit_contact_form", views.submit_contact_form, name="submit_contact_form"),
    path("about/", views.about, name="about"),
    path("help/", views.help, name="help"),
]
