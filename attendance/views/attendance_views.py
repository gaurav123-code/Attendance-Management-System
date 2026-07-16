from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
# from attendance.forms import EmployeeForm

from attendance.models import Attendance, Employee


def calculate_working_hours(attendance):
    if attendance.check_in and attendance.check_out:
        check_in = datetime.combine(
            attendance.attendance_date,
            attendance.check_in,
        )

        check_out = datetime.combine(
            attendance.attendance_date,
            attendance.check_out,
        )

        duration = check_out - check_in

        total_seconds = int(duration.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        return f"{hours}h {minutes}m"

    return "--"


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")

    employee = (
        Employee.objects
        .select_related("department", "user")
        .filter(user=request.user)
        .first()
    )

    today_attendance = None
    working_hours = "--"
    attendance_history = []

    if employee:
        today_attendance = Attendance.objects.filter(
            employee=employee,
            attendance_date=date.today(),
        ).first()

        if today_attendance:
            working_hours = calculate_working_hours(
                today_attendance
            )

        attendance_history = (
            Attendance.objects
            .filter(employee=employee)
            .order_by("-attendance_date")[:30]
        )

    context = {
        "employee": employee,
        "today_attendance": today_attendance,
        "working_hours": working_hours,
        "attendance_history": attendance_history,
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )


@login_required
def check_in(request):
    if request.method != "POST":
        return redirect("dashboard")

    employee = get_object_or_404(
        Employee,
        user=request.user,
    )

    attendance, created = (
        Attendance.objects.get_or_create(
            employee=employee,
            attendance_date=date.today(),
        )
    )

    if attendance.check_in:
        messages.warning(
            request,
            "You have already checked in today.",
        )
        return redirect("dashboard")

    attendance.check_in = (
        timezone.localtime()
        .time()
        .replace(microsecond=0)
    )

    attendance.save()

    messages.success(
        request,
        "Check In successful.",
    )

    return redirect("dashboard")


@login_required
def check_out(request):

    if request.method != "POST":
        return redirect("dashboard")

    employee = get_object_or_404(
        Employee,
        user=request.user,
    )

    attendance = Attendance.objects.filter(
        employee=employee,
        attendance_date=date.today(),
    ).first()

    if not attendance:
        messages.warning(
            request,
            "Please check in first.",
        )
        return redirect("dashboard")

    if attendance.check_out:
        messages.warning(
            request,
            "You have already checked out today.",
        )
        return redirect("dashboard")

    attendance.check_out = (
        timezone.localtime()
        .time()
        .replace(microsecond=0)
    )

    attendance.save()

    messages.success(
        request,
        "Check Out successful.",
    )

    return redirect("dashboard")