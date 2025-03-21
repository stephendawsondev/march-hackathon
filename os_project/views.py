from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Project, ProjectInterest
from .forms import ProjectForm, ProjectInterestForm, ProjectSearchForm


# List views
class ProjectListView(ListView):
    model = Project
    template_name = "os_project/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProjectSearchForm(self.request.GET)

        if form.is_valid():
            search = form.cleaned_data.get("search")
            category = form.cleaned_data.get("category")
            tags = form.cleaned_data.get("tags")
            status = form.cleaned_data.get("status")
            difficulty = form.cleaned_data.get("difficulty")

            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search)
                    | Q(description__icontains=search)
                    | Q(technologies__icontains=search)
                )

            if category:
                queryset = queryset.filter(category=category)

            if tags:
                queryset = queryset.filter(tags__in=tags).distinct()

            if status:
                queryset = queryset.filter(status=status)

            if difficulty:
                queryset = queryset.filter(difficulty=difficulty)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = ProjectSearchForm(self.request.GET)
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "os_project/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the user has already expressed interest in this project
        user_interested = False
        if self.request.user.is_authenticated:
            user_interested = ProjectInterest.objects.filter(
                project=self.object, user_id=self.request.user.id
            ).exists()

        context["user_interested"] = user_interested
        context["interest_form"] = ProjectInterestForm()

        # Get all users who have expressed interest
        context["interest_count"] = ProjectInterest.objects.filter(
            project=self.object
        ).count()

        return context


# Create, Update, Delete views
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "os_project/project_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        # Set the owner to the current user
        form.instance.owner_id = self.request.user.id
        messages.success(self.request, "Project created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "os_project/project_form.html"

    def get_queryset(self):
        # Only allow users to edit their own projects
        return Project.objects.filter(owner_id=self.request.user.id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Project updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "os_project/project_confirm_delete.html"
    success_url = reverse_lazy("project_list")

    def get_queryset(self):
        # Only allow users to delete their own projects
        return Project.objects.filter(owner_id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        project = self.get_object()

        # Check if a WIT is assigned to this project
        if project.assigned_wit_id is not None:
            messages.error(
                request,
                "Cannot delete a project that has a Woman in Tech assigned to it.",
            )
            return redirect("project_detail", pk=project.pk)

        messages.success(request, "Project deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Project Interest
@login_required
def express_interest(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Check if user has already expressed interest
    existing_interest = ProjectInterest.objects.filter(
        project=project, user_id=request.user.id
    ).exists()

    if existing_interest:
        messages.info(request, "You have already expressed interest in this project")
        return redirect("project_detail", pk=project_id)

    if request.method == "POST":
        form = ProjectInterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.project = project
            interest.user_id = request.user.id
            interest.save()

            messages.success(request, "Your interest has been recorded")
            return redirect("project_detail", pk=project_id)
    else:
        form = ProjectInterestForm()

    return render(
        request, "os_project/express_interest.html", {"form": form, "project": project}
    )


@login_required
def withdraw_interest(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    interest = ProjectInterest.objects.filter(
        project=project, user_id=request.user.id
    ).first()

    if interest:
        interest.delete()
        messages.success(request, "Your interest has been withdrawn")
    else:
        messages.error(request, "You have not expressed interest in this project")

    return redirect("project_detail", pk=project_id)


# Dashboard views for project owners
@login_required
def project_dashboard(request):
    # Get projects owned by the current user
    owned_projects = Project.objects.filter(owner_id=request.user.id)

    return render(
        request, "os_project/project_dashboard.html", {"owned_projects": owned_projects}
    )


@login_required
def project_interested_users(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Check if user is the owner
    if project.owner_id != request.user.id:
        messages.error(request, "You are not authorized to view this page")
        return redirect("project_list")

    interested_users = ProjectInterest.objects.filter(project=project)

    return render(
        request,
        "os_project/project_interested_users.html",
        {"project": project, "interested_users": interested_users},
    )


@login_required
def select_wit(request, project_id, interest_id):
    project = get_object_or_404(Project, pk=project_id)
    interest = get_object_or_404(ProjectInterest, pk=interest_id, project=project)

    # Check if user is the owner
    if project.owner_id != request.user.id:
        messages.error(request, "You are not authorized to perform this action")
        return redirect("project_list")

    # Check if a WIT is already assigned
    if project.assigned_wit_id is not None:
        messages.error(request, "A Woman in Tech is already assigned to this project")
        return redirect("project_detail", pk=project_id)

    # Assign the WIT
    project.assigned_wit_id = interest.user_id
    project.status = "ASSIGNED"
    project.save()

    messages.success(request, "Woman in Tech has been assigned to the project")
    return redirect("project_detail", pk=project_id)
