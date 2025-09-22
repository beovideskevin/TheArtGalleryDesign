from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("painting", views.painting, name="painting"),
    path("illustration", views.illustration, name="illustration"),
    path("design", views.design, name="design"),
    path("photography", views.photography, name="photography"),
    path("installation", views.installation, name="installation"),
    path("recent", views.recent, name="recent"),
    path("gallery/<str:cat>", views.gallery, name="gallery"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
]