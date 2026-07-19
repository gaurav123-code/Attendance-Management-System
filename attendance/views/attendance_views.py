from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..decorators import admin_required
from ..models import Attendance, Employee


@login_required
def dashboard(request):
    # Superuser should never have an Employee record.
    if request.user.is_superuser:
        return redirect("admin_dashboard")

    employee = get_object_or_404(
        Employee,
        user=request.user
    )

    today = timezone.localdate()

    attendance = Attendance.objects.filter(
        employee=employee,
        attendance_date=today
    ).first()

    context = {
        "employee": employee,
        "attendance": attendance,
    }

    return render(
        request,
        "dashboard/home.html",
        context
    )


@login_required
def check_in(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")

    employee = get_object_or_404(
        Employee,
        user=request.user
    )

    today = timezone.localdate()

    existing_attendance = Attendance.objects.filter(
        employee=employee,
        attendance_date=today
    ).first()

    if existing_attendance:
        messages.warning(
            request,
            "You have already checked in today."
        )
        return redirect("dashboard")

    attendance = Attendance.objects.create(
        employee=employee,
        attendance_date=today,
        check_in=timezone.localtime().time(),
    )

    attendance.status = attendance.calculate_status()
    attendance.save()

    messages.success(
        request,
        "Check-in successful."
    )

    return redirect("dashboard")


@login_required
def check_out(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")

    employee = get_object_or_404(
        Employee,
        user=request.user
    )

    today = timezone.localdate()

    attendance = Attendance.objects.filter(
        employee=employee,
        attendance_date=today
    ).first()

    if not attendance:
        messages.error(
            request,
            "Please check-in first."
        )
        return redirect("dashboard")

    if attendance.check_out:
        messages.warning(
            request,
            "You have already checked out."
        )
        return redirect("dashboard")

    attendance.check_out = timezone.localtime().time()
    attendance.working_hours = attendance.calculate_working_hours()
    attendance.save()

    messages.success(
        request,
        "Check-out successful."
    )

    return redirect("dashboard")


@login_required
def my_attendance(request):

    if request.user.is_superuser:
        return redirect("admin_dashboard")


    employee = get_object_or_404(
        Employee,
        user=request.user
    )


    attendance_records = Attendance.objects.filter(
        employee=employee
    ).order_by(
        "-attendance_date"
    )


    total_days = attendance_records.count()


    present_days = attendance_records.filter(
        status="PRESENT"
    ).count()


    absent_days = attendance_records.filter(
        status="ABSENT"
    ).count()



    context = {

        "employee": employee,

        "attendance_records": attendance_records,

        "total_days": total_days,

        "present_days": present_days,

        "absent_days": absent_days,

    }


    return render(
        request,
        "attendance/my_attendance.html",
        context
    )


@login_required
@admin_required
def attendance_list(request):
    attendance_records = Attendance.objects.select_related(
        "employee",
        "employee__department"
    ).order_by(
        "-attendance_date"
    )

    context = {
        "attendance_records": attendance_records
    }

    return render(
        request,
        "attendance/attendance_list.html",
        context
    )


@login_required
@admin_required
def attendance_manage(request):
    today = timezone.localdate()

    attendance_records = Attendance.objects.filter(
        attendance_date=today
    ).select_related(
        "employee"
    )

    context = {
        "attendance_records": attendance_records,
        "today": today
    }

    return render(
        request,
        "attendance/attendance_manage.html",
        context
    )


@login_required
@admin_required
def mark_attendance(request):
    employees = Employee.objects.filter(
        is_active=True
    )

    today = timezone.localdate()

    if request.method == "POST":
        employee_id = request.POST.get("employee")
        status = request.POST.get("status")

        employee = get_object_or_404(
            Employee,
            id=employee_id
        )

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            attendance_date=today
        )

        attendance.status = status
        attendance.save(update_fields=["status"])

        messages.success(
            request,
            "Attendance marked successfully."
        )

        return redirect("attendance_manage")

    context = {
        "employees": employees
    }

    return render(
        request,
        "attendance/mark_attendance.html",
        context
    )


@login_required
@admin_required
def absent_mark(request):
    today = timezone.localdate()

    if timezone.localtime().time() < time(18, 0):
        messages.warning(
            request,
            "Employees can be marked absent only after 6:00 PM."
        )
        return redirect("attendance_manage")

    employees = Employee.objects.filter(
        is_active=True
    )

    for employee in employees:
        Attendance.objects.get_or_create(
            employee=employee,
            attendance_date=today,
            defaults={
                "status": "ABSENT"
            }
        )

    messages.success(
        request,
        "Absent marked for remaining employees."
    )

    return redirect("attendance_manage")


@login_required
@admin_required
def attendance_detail(request, id):
    attendance = get_object_or_404(
        Attendance,
        id=id
    )

    context = {
        "attendance": attendance
    }

    return render(
        request,
        "attendance/attendance_detail.html",
        context
    )