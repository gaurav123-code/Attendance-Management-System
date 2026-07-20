from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from ..decorators import admin_required
from ..models import Attendance, Department, Employee

from datetime import timedelta




@login_required
@admin_required
def report_dashboard(request):

    today = timezone.now().date()

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

    half_day_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.HALF_DAY,
    ).count()

    absent_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.ABSENT,
    ).count()


    # ===============================
    # Last 30 Days Attendance Trend
    # ===============================

    start_date = today - timedelta(days=29)

    trend_labels = []
    present_data = []
    late_data = []
    half_day_data = []
    absent_data = []
    
    department_labels = []
    department_counts = []
    
    working_hours_labels = []
    working_hours_data = []


    for i in range(30):

        current_date = start_date + timedelta(
            days=i
        )

        trend_labels.append(
            current_date.strftime("%d %b")
        )


        present_count = Attendance.objects.filter(
            attendance_date=current_date,
            status=Attendance.PRESENT,
        ).count()


        late_count = Attendance.objects.filter(
            attendance_date=current_date,
            status=Attendance.LATE,
        ).count()


        half_day_count = Attendance.objects.filter(
            attendance_date=current_date,
            status=Attendance.HALF_DAY,
        ).count()


        absent_count = Attendance.objects.filter(
            attendance_date=current_date,
            status=Attendance.ABSENT,
        ).count()


        present_data.append(
            present_count
        )

        late_data.append(
            late_count
        )

        half_day_data.append(
            half_day_count
        )

        absent_data.append(
            absent_count
        )



    # ===============================
    # Department Employee Distribution
    # ===============================

    department_labels = []
    department_counts = []


    departments = Department.objects.order_by("name")

    for department in departments:

        department_labels.append(
            department.name
        )

        department_counts.append(
            department.employees.filter(
                is_active=True
            ).count()
        )



    # ===============================
    # Working Hours Analysis
    # ===============================

    working_hours_labels = []
    working_hours_data = []


    recent_attendance = Attendance.objects.filter(
        working_hours__isnull=False
    ).select_related(
        "employee"
    ).order_by(
        "-attendance_date"
    )[:10]


    for attendance in recent_attendance:

        working_hours_labels.append(
            f"{attendance.employee.employee_id} - {attendance.employee.first_name}"
        )


        total_seconds = (
            attendance.working_hours.total_seconds()
        )


        hours = round(
            total_seconds / 3600,
            2
        )


        working_hours_data.append(
            hours
        )



    context = {

        "total_employees": total_employees,

        "present_today": present_today,

        "late_today": late_today,

        "half_day_today": half_day_today,

        "absent_today": absent_today,


        "trend_labels": trend_labels,

        "present_data": present_data,

        "late_data": late_data,

        "half_day_data": half_day_data,

        "absent_data": absent_data,


        "department_labels": department_labels,

        "department_counts": department_counts,


        "working_hours_labels": working_hours_labels,

        "working_hours_data": working_hours_data,

    }


    return render(
        request,
        "reports/dashboard.html",
        context
    )




@login_required
@admin_required
def late_report(request):

    selected_date = request.GET.get(
        "date"
    )

    if selected_date:

        try:

            report_date = datetime.strptime(
                selected_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            report_date = timezone.now().date()

    else:

        report_date = timezone.now().date()


    late_attendance = Attendance.objects.filter(
        attendance_date=report_date,
        status=Attendance.LATE
    ).select_related(
        "employee",
        "employee__department"
    ).order_by(
        "check_in"
    )



    context = {

        "late_attendance": late_attendance,

        "late_count": late_attendance.count(),

        "selected_date": report_date,

    }



    return render(
        request,
        "attendance/late_report.html",
        context
    )




@login_required
@admin_required
def absent_report(request):

    selected_date = request.GET.get(
        "date"
    )


    if selected_date:

        try:

            report_date = datetime.strptime(
                selected_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            report_date = timezone.now().date()

    else:

        report_date = timezone.now().date()



    absent_attendance = Attendance.objects.filter(
        attendance_date=report_date,
        status=Attendance.ABSENT
    ).select_related(
        "employee",
        "employee__department"
    ).order_by(
        "employee__first_name"
    )



    context = {

        "absent_attendance": absent_attendance,

        "absent_count": absent_attendance.count(),

        "selected_date": report_date,

    }



    return render(
        request,
        "attendance/absent_report.html",
        context
    )





@login_required
@admin_required
def working_hours_report(request):

    selected_date = request.GET.get(
        "date"
    )


    if selected_date:

        try:

            report_date = datetime.strptime(
                selected_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            report_date = timezone.now().date()

    else:

        report_date = timezone.now().date()


    working_hours = Attendance.objects.filter(
        attendance_date=report_date,
        working_hours__isnull=False
    ).select_related(
        "employee",
        "employee__department"
    ).order_by(
        "-working_hours"
    )



    total_working_hours = 0

    employee_count = working_hours.count()


    for attendance in working_hours:

        if attendance.working_hours:

            total_working_hours += (
                attendance.working_hours.total_seconds()
            )



    average_working_hours = 0


    if employee_count:

        average_working_hours = round(
            (
                total_working_hours / employee_count
            ) / 3600,
            2
        )



    context = {

        "working_hours": working_hours,

        "working_count": employee_count,

        "average_working_hours": average_working_hours,

        "selected_date": report_date,

    }



    return render(
        request,
        "attendance/working_hours_report.html",
        context
    )






@login_required
@admin_required
def department_attendance_report(request):

    selected_date = request.GET.get(
        "date"
    )

    selected_department = request.GET.get(
        "department"
    )



    if selected_date:

        try:

            report_date = datetime.strptime(
                selected_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            report_date = timezone.now().date()

    else:

        report_date = timezone.now().date()

    
    present_count = Attendance.objects.filter(
    attendance_date=report_date,
    status__in=[
        Attendance.PRESENT,
        Attendance.LATE,
        Attendance.HALF_DAY,
    ],
    ).count()

    absent_count = Attendance.objects.filter(
        attendance_date=report_date,
        status=Attendance.ABSENT,
    ).count()

    departments = Department.objects.order_by("name")



    department_report = departments.annotate(

        total_employees=Count(
            "employees",
            filter=Q(
                employees__is_active=True
            ),
            distinct=True
        ),


        present=Count(
            "employees__attendances",
            filter=Q(
                employees__attendances__attendance_date=report_date,
                employees__attendances__status=Attendance.PRESENT
            ),
            distinct=True
        ),


        late=Count(
            "employees__attendances",
            filter=Q(
                employees__attendances__attendance_date=report_date,
                employees__attendances__status=Attendance.LATE
            ),
            distinct=True
        ),


        half_day=Count(
            "employees__attendances",
            filter=Q(
                employees__attendances__attendance_date=report_date,
                employees__attendances__status=Attendance.HALF_DAY
            ),
            distinct=True
        ),


        absent=Count(
            "employees__attendances",
            filter=Q(
                employees__attendances__attendance_date=report_date,
                employees__attendances__status=Attendance.ABSENT
            ),
            distinct=True
        ),

    )
    
    for department in department_report:

        attended = (
            department.present
            + department.late
            + department.half_day
        )

        if department.total_employees:

            department.attendance_percentage = round(
                (attended / department.total_employees) * 100,
                2
            )

        else:

            department.attendance_percentage = 0



    if selected_department:

        department_report = department_report.filter(
            id=selected_department
        )



    context = {

        "departments": departments,

        "department_report": department_report,

        "department_count": department_report.count(),

        "total_employees": Employee.objects.filter(
            is_active=True
        ).count(),

        "selected_date": report_date,

        "selected_department": selected_department,
        
        "present_count": present_count,

        "absent_count": absent_count,

    }



    return render(
        request,
        "attendance/department_attendance_report.html",
        context
    )






@login_required
@admin_required
def dashboard_stats(request):

    today = timezone.now().date()

    total_employees = Employee.objects.filter(
        is_active=True
    ).count()

    active_employees = Employee.objects.filter(
        is_active=True
    ).count()

    inactive_employees = Employee.objects.filter(
        is_active=False
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

    half_day_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.HALF_DAY,
    ).count()

    absent_today = Attendance.objects.filter(
        attendance_date=today,
        status=Attendance.ABSENT,
    ).count()

    # ====================================
    # Department Performance
    # ====================================

    department_stats = []

    departments = Department.objects.prefetch_related(
        "employees"
    ).order_by(
        "name"
    )

    for department in departments:

        employee_count = department.employees.filter(
            is_active=True
        ).count()

        attended_today = Attendance.objects.filter(
            employee__department=department,
            employee__is_active=True,
            attendance_date=today,
            status__in=[
                Attendance.PRESENT,
                Attendance.LATE,
                Attendance.HALF_DAY,
            ]
        ).count()

        if employee_count > 0:

            attendance_percentage = round(
                (attended_today / employee_count) * 100,
                2
            )

        else:

            attendance_percentage = 0

        department.employee_count = employee_count
        department.attendance_percentage = attendance_percentage

        department_stats.append(
            department
        )

    # ====================================
    # Monthly Summary
    # ====================================

    monthly_stats = []

    present_count = Attendance.objects.filter(
        attendance_date__month=today.month,
        attendance_date__year=today.year,
        status=Attendance.PRESENT,
    ).count()

    late_count = Attendance.objects.filter(
        attendance_date__month=today.month,
        attendance_date__year=today.year,
        status=Attendance.LATE,
    ).count()

    absent_count = Attendance.objects.filter(
        attendance_date__month=today.month,
        attendance_date__year=today.year,
        status=Attendance.ABSENT,
    ).count()

    monthly_stats.append(
        {
            "month": today.strftime("%B %Y"),
            "present": present_count,
            "late": late_count,
            "absent": absent_count,
        }
    )

    context = {

        "total_employees": total_employees,

        "active_employees": active_employees,

        "inactive_employees": inactive_employees,

        "present_today": present_today,

        "late_today": late_today,

        "half_day_today": half_day_today,

        "absent_today": absent_today,

        "department_stats": department_stats,

        "monthly_stats": monthly_stats,

    }

    return render(
        request,
        "attendance/dashboard_stats.html",
        context
    )