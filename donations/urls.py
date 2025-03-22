from django.urls import path

from . import views

urlpatterns = [
    # paths goes here
    path("", views.donations, name="donations"),
    path("cache_donation_data/", views.cache_donation_data, name="cache_donation_data"),
]
