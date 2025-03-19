from django.contrib import admin
from django.urls import path, include
from django.views import defaults as default_views

handler404 = "march_hackathon_placeholder.views.custom_page_not_found"
handler500 = "march_hackathon_placeholder.views.custom_server_error"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("profile/", include("user_profile.urls")),
    path("", include("home.urls")),
]
