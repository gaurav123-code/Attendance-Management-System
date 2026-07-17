from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View


class CustomLoginView(LoginView):
    """
    Custom login view for Admin and Employee.
    """

    template_name = "registration/login.html"

    redirect_authenticated_user = True

    def get_success_url(self):

        if self.request.user.is_superuser:
            return reverse_lazy("admin_dashboard")

        return reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            if request.user.is_superuser:
                return redirect("admin_dashboard")

            return redirect("dashboard")

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )


class CustomLogoutView(View):
    """
    Custom logout view.
    """

    def post(self, request):

        logout(request)

        messages.success(
            request,
            "You have been logged out successfully.",
        )

        return redirect("login")