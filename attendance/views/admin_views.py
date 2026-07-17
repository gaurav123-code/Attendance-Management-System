from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from attendance.models import Attendance, Employee


@login_required
def admin_dashboard(request):
    """
    Admin Dashboard

    Only Django Superusers are allowed
    to access this page.
    """

    if not request.user.is_superuser:
        messages.error(
            request,
            "You are not authorized to access the Admin Dashboard.",
        )
        return redirect("dashboard")

    today = date.today()

    total_employees = Employee.objects.count()

    present_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.AttendanceStatus.PRESENT,
    ).count()

    late_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.AttendanceStatus.LATE,
    ).count()

    half_day_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.AttendanceStatus.HALF_DAY,
    ).count()

    absent_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.AttendanceStatus.ABSENT,
    ).count()

    leave_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.AttendanceStatus.LEAVE,
    ).count()

    recent_attendance = (
        Attendance.objects
        .select_related(
            "employee",
            "employee__department",
        )
        .order_by(
            "-attendance_date",
            "-created_at",
        )[:10]
    )

    context = {
        "total_employees": total_employees,
        "present_today": present_today,
        "late_today": late_today,
        "half_day_today": half_day_today,
        "absent_today": absent_today,
        "leave_today": leave_today,
        "recent_attendance": recent_attendance,
    }

    return render(
        request,
        "admin_dashboard/home.html",
        context,
    )