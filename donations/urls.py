from django.urls import path

from . import views

urlpatterns = [
    # paths goes here
    path("", views.donations, name="donations"),
]
