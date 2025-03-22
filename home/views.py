from django.shortcuts import render


def home(request):
    return render(request, "home/home.html")


def team(request):
    return render(request, "home/team.html")
