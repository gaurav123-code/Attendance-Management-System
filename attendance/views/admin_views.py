from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from ..models import Employee
from django.db.models import Q

from ..models import (
    Attendance,
    Employee,
)





# ==========================
# Admin Dashboard
# ==========================

def admin_dashboard(request):

    today = timezone.localdate()

    total_employees = Employee.objects.filter(
        is_active=True
    ).count()

    present_today = Attendance.objects.filter(
        attendance_date=today,
        status__in=[
            Attendance.PRESENT,
            Attendance.LATE,
            Attendance.HALF_DAY,
        ],
    ).count()

    late_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.LATE,
    ).count()

    absent_today = max(
        total_employees - present_today,
        0,
    )

    recent_attendance = (
        Attendance.objects.filter(
            attendance_date=today
        )
        .select_related(
            "employee",
            "employee__department",
        )
        .order_by(
            "-updated_at",
        )[:10]
    )
        

    context = {

        "total_employees": total_employees,

        "present_today": present_today,

        "late_today": late_today,

        "absent_today": absent_today,

        "recent_attendance": recent_attendance,

    }

    return render(
        request,
        "admin_dashboard/home.html",
        context,
    )







# ==========================
# Custom Login
# ==========================

class CustomLoginView(LoginView):


    template_name = "registration/login.html"



    def form_valid(self, form):


        response = super().form_valid(
            form
        )


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








# ==========================
# Logout
# ==========================

class CustomLogoutView(LogoutView):


    next_page = "login"








# ==========================
# Password Reset
# ==========================

class CustomPasswordResetView(PasswordResetView):


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









# ==========================
# Password Change
# ==========================

class CustomPasswordChangeView(
    PasswordChangeView
):


    template_name = (
        "registration/change_password.html"
    )


    success_url = reverse_lazy(
        "dashboard"
    )



    def form_valid(self, form):


        response = super().form_valid(
            form
        )



        user = self.request.user



        try:


            employee = Employee.objects.get(
                user=user
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