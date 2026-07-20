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
        "today_attendance": attendance,
        "today": today,
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

    employees = Employee.objects.filter(
        is_active=True
    )

    employee = request.GET.get("employee")
    date = request.GET.get("date")
    status = request.GET.get("status")

    if employee:
        attendance_records = attendance_records.filter(
            employee_id=employee
        )

    if date:
        attendance_records = attendance_records.filter(
            attendance_date=date
        )

    if status:
        attendance_records = attendance_records.filter(
            status=status
        )

    context = {
        "attendance_records": attendance_records,
        "employees": employees,
        "status_choices": Attendance.STATUS_CHOICES,
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

    attendances = (
        Attendance.objects.filter(
            attendance_date=today
        )
        .select_related(
            "employee",
            "employee__department",
        )
        .order_by("employee__first_name")
    )

    total_employees = Employee.objects.filter(
        is_active=True
    ).count()

    present_today = attendances.filter(
        status=Attendance.PRESENT
    ).count()

    late_today = attendances.filter(
        status=Attendance.LATE
    ).count()

    absent_today = (
        total_employees
        - attendances.count()
    ) + attendances.filter(
        status=Attendance.ABSENT
    ).count()

    context = {

        "today": today,

        "attendances": attendances,

        "total_employees": total_employees,

        "present_today": present_today,

        "late_today": late_today,

        "absent_today": absent_today,

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

        employee = get_object_or_404(
            Employee,
            id=employee_id
        )


        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            attendance_date=today
        )


        attendance.check_in = request.POST.get(
            "check_in"
        ) or None


        attendance.check_out = request.POST.get(
            "check_out"
        ) or None


        attendance.status = request.POST.get(
            "status"
        )


        attendance.remarks = request.POST.get(
            "remarks"
        )


        if attendance.check_in:

            attendance.status = attendance.calculate_status()


        if attendance.check_in and attendance.check_out:

            attendance.working_hours = (
                attendance.calculate_working_hours()
            )


        attendance.save()


        messages.success(
            request,
            "Manual attendance marked successfully."
        )


        return redirect(
            "attendance_manage"
        )


    context = {

        "employees": employees,

        "status_choices": Attendance.STATUS_CHOICES,

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