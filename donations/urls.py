from django.urls import path

from . import views

urlpatterns = [
    # paths goes here
    path("donations/", views.donations, name="donations"),
]
