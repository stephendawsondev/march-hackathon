from django.urls import path
from . import views

urlpatterns = [

    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),

]
