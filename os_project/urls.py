from django.urls import path
from . import views

urlpatterns = [
    # List and detail views
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/update/", views.ProjectUpdateView.as_view(), name="project_update"),
    path("<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),
]
