from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from functools import wraps


def os_maintainer_required(view_func):
    """
    Decorator for views that checks that the user is an OS Maintainer,
    redirecting to the project list page if necessary.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("account_login")

        # Check if user has an OS Maintainer profile
        try:
            if (
                hasattr(request.user, "os_maintainer_profile")
                and request.user.os_maintainer_profile
            ):
                return view_func(request, *args, **kwargs)
        except:
            pass

        # If user is not an OS Maintainer, show an error message and redirect
        messages.error(request, "Only Open Source Maintainers can access this page.")
        return redirect("project_list")

    return _wrapped_view


class OSMaintainerRequiredMixin:
    """
    Mixin for class-based views that checks if the user is an OS Maintainer.
    """

    def dispatch(self, request, *args, **kwargs):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect("account_login")

        # Check if user has an OS Maintainer profile
        try:
            if (
                hasattr(request.user, "os_maintainer_profile")
                and request.user.os_maintainer_profile
            ):
                return super().dispatch(request, *args, **kwargs)
        except:
            pass

        # If user is not an OS Maintainer, show an error message and redirect
        messages.error(request, "Only Open Source Maintainers can access this page.")
        return redirect("project_list")
