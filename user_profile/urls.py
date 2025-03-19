# profile/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.profile_update, name='profile_update'),
    path('delete/', views.profile_delete, name='profile_delete'),
    path('<str:username>/', views.profile_detail, name='profile_detail'),
]
