from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from attendance.views.auth_views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordResetCompleteView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetView,
)


def home_redirect(request):
    return redirect("login")


urlpatterns = [

    # ==========================================================
    # Home
    # ==========================================================

    path(
        "",
        home_redirect,
        name="home",
    ),

    # ==========================================================
    # Django Admin
    # ==========================================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ==========================================================
    # Authentication
    # ==========================================================

    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        CustomLogoutView.as_view(),
        name="logout",
    ),

    # ==========================================================
    # Password Reset
    # ==========================================================

    path(
        "password-reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),

    path(
        "password-reset-confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    path(
        "password-reset-complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    # ==========================================================
    # Attendance Application
    # ==========================================================

    path(
        "",
        include("attendance.urls"),
    ),
]