import logging
import time
import uuid

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
)

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone

from ..forms import (
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
)

from ..models import Employee

logger = logging.getLogger(__name__)


# ==========================================================
# Employee ID Authentication Form
# ==========================================================

class EmployeeIDAuthenticationForm(forms.Form):

    username = forms.CharField(
        label="Employee ID",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Employee ID",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password",
                "autocomplete": "current-password",
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super().clean()

        login_id = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if login_id and password:

            try:
                employee = Employee.objects.get(
                    employee_id=login_id
                )

                username = employee.user.username

            except Employee.DoesNotExist:
                username = login_id

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid Employee ID or Password."
                )

            if not self.user_cache.is_active:
                raise forms.ValidationError(
                    "This account is inactive."
                )

        return cleaned_data

    def get_user(self):
        return self.user_cache


# ==========================================================
# Login View
# ==========================================================

class CustomLoginView(LoginView):

    template_name = "registration/login.html"

    authentication_form = EmployeeIDAuthenticationForm

    redirect_authenticated_user = True


    def form_valid(self, form):

        response = super().form_valid(form)

        user = self.request.user


        if user.is_superuser:
            return redirect(
                "admin_dashboard"
            )


        try:

            employee = Employee.objects.get(
                user=user
            )


            if employee.must_change_password:

                return redirect(
                    "change_password"
                )


        except Employee.DoesNotExist:
            pass


        return redirect(
            "dashboard"
        )



# ==========================================================
# Global Password Change Protection
# ==========================================================

def password_change_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:

            if request.user.is_superuser:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )


            try:

                employee = Employee.objects.get(
                    user=request.user
                )


                if employee.must_change_password:

                    if request.resolver_match.url_name != "change_password":

                        return redirect(
                            "change_password"
                        )


            except Employee.DoesNotExist:
                pass


        return view_func(
            request,
            *args,
            **kwargs
        )


    return wrapper



# ==========================================================
# Logout View
# ==========================================================

class CustomLogoutView(LogoutView):

    next_page = reverse_lazy(
        "login"
    )


    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        messages.success(
            request,
            "You have been logged out successfully."
        )

        return super().dispatch(
            request,
            *args,
            **kwargs
        )



# ==========================================================
# Password Reset
# ==========================================================

class CustomPasswordResetView(
    PasswordResetView
):

    form_class = CustomPasswordResetForm

    template_name = (
        "registration/password_reset_form.html"
    )

    email_template_name = (
        "registration/password_reset_email.html"
    )

    subject_template_name = (
        "registration/password_reset_subject.txt"
    )

    success_url = reverse_lazy(
        "password_reset_done"
    )


    def form_valid(self, form):

        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        email = form.cleaned_data.get(
            "email"
        )


        logger.info("=" * 70)
        logger.info(
            "[RESET %s] PASSWORD RESET START",
            request_id
        )

        logger.info(
            "[RESET %s] Submitted Email: %s",
            request_id,
            email
        )


        try:

            response = super().form_valid(
                form
            )


            elapsed = time.perf_counter() - start_time


            logger.info(
                "[RESET %s] Email sent successfully",
                request_id
            )


            logger.info(
                "[RESET %s] Completed in %.3f seconds",
                request_id,
                elapsed
            )


            logger.info("=" * 70)


            return response


        except Exception as error:


            elapsed = time.perf_counter() - start_time


            logger.exception(
                "[RESET %s] FAILED after %.3f seconds : %s",
                request_id,
                elapsed,
                error
            )


            logger.info("=" * 70)


            raise


class CustomPasswordResetDoneView(
    PasswordResetDoneView
):

    template_name = (
        "registration/password_reset_done.html"
    )



class CustomPasswordResetConfirmView(
    PasswordResetConfirmView
):

    template_name = (
        "registration/password_reset_confirm.html"
    )

    success_url = reverse_lazy(
        "password_reset_complete"
    )



class CustomPasswordResetCompleteView(
    PasswordResetCompleteView
):

    template_name = (
        "registration/password_reset_complete.html"
    )



# ==========================================================
# Password Change
# ==========================================================

class CustomPasswordChangeView(
    PasswordChangeView
):

    template_name = (
        "registration/change_password.html"
    )

    success_url = reverse_lazy(
        "dashboard"
    )
    
    form_class = CustomPasswordChangeForm


    def form_valid(self, form):

        response = super().form_valid(
            form
        )


        try:

            employee = Employee.objects.get(
                user=self.request.user
            )


            employee.must_change_password = False

            employee.password_changed_at = (
                timezone.now()
            )

            employee.save()


        except Employee.DoesNotExist:
            pass



        messages.success(
            self.request,
            "Password changed successfully."
        )


        return response



# ==========================================================
# Wrapper Function
# ==========================================================

def change_password(request):

    return CustomPasswordChangeView.as_view()(
        request
    )