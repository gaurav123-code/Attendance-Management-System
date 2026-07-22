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
    current_time = timezone.localtime().time()

    if current_time > time(15, 0):

        messages.error(
            request,
            "Check-in is not allowed after 3:00 PM."
        )

        return redirect("dashboard")


    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        attendance_date=today,
        defaults={
            "check_in": timezone.localtime().time(),
        }
    )


    # Already checked in
    if not created and attendance.check_in:

        messages.warning(
            request,
            "You have already checked in today."
        )

        return redirect("dashboard")


    # Update existing ABSENT record
    attendance.check_in = timezone.localtime().time()
    attendance.status = attendance.calculate_status()
    attendance.remarks = ""

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
    )

    status = request.GET.get("status")

    if status:
        attendance_records = attendance_records.filter(
            status=status
        )

    attendance_records = attendance_records.order_by(
        "-attendance_date"
    )

    total_days = Attendance.objects.filter(
        employee=employee
    ).count()

    attendance_days = Attendance.objects.filter(
        employee=employee,
        status__in=[
            Attendance.PRESENT,
            Attendance.LATE,
            Attendance.HALF_DAY,
        ]
    ).count()

    late_days = Attendance.objects.filter(
        employee=employee,
        status=Attendance.LATE
    ).count()

    half_day_days = Attendance.objects.filter(
        employee=employee,
        status=Attendance.HALF_DAY
    ).count()

    absent_days = Attendance.objects.filter(
        employee=employee,
        status=Attendance.ABSENT
    ).count()

    context = {

        "employee": employee,

        "attendance_records": attendance_records,

        "total_days": total_days,

        "attendance_days": attendance_days,

        "late_days": late_days,

        "half_day_days": half_day_days,

        "absent_days": absent_days,

        "selected_status": status,

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


        check_in = request.POST.get(
            "check_in"
        )

        check_out = request.POST.get(
            "check_out"
        )


        if check_in:
            attendance.check_in = datetime.strptime(
                check_in,
                "%H:%M"
            ).time()
        else:
            attendance.check_in = None


        if check_out:
            attendance.check_out = datetime.strptime(
                check_out,
                "%H:%M"
            ).time()
        else:
            attendance.check_out = None

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

    if timezone.localtime().time() < time(15, 0):
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
                "status": Attendance.ABSENT,
                "remarks": "Automatically marked absent"
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