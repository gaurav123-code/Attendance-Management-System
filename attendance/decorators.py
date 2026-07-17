from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def admin_required(view_func):
    """
    Allow access only to authenticated
    Django Superusers.
    """

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_superuser:

            messages.error(
                request,
                "You are not authorized to access this page.",
            )

            return redirect("dashboard")

        return view_func(
            request,
            *args,
            **kwargs,
        )

    return wrapper