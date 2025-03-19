# profile/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm


def profile_detail(request, username):
    """View for displaying a user profile"""
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    context = {
        'profile_user': user,
        'profile': profile,
    }
    return render(request, 'user_profile/profile_detail.html', context)


@login_required
def profile_update(request):
    """View for updating a profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile_detail', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user_profile/profile_form.html', context)


@login_required
def profile_delete(request):
    """View for confirming account deletion"""
    if request.method == 'POST':
        # Delete the user (which will cascade delete the profile)
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    return render(request, 'user_profile/profile_confirm_delete.html')
