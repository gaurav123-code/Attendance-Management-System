from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from django.shortcuts import render
from django.utils import timezone

from ..decorators import admin_required
from ..models import Attendance, Department, Employee



@login_required
@admin_required
def report_dashboard(request):

    today = timezone.now().date()

    context = {

        "total_employees": Employee.objects.filter(
            is_active=True
        ).count(),


        "present_today": Attendance.objects.filter(
            attendance_date=today,
            status__in=["PRESENT", "LATE", "HALF_DAY"]
        ).count(),


        "late_today": Attendance.objects.filter(
            attendance_date=today,
            status="LATE"
        ).count(),


        "absent_today": Attendance.objects.filter(
            attendance_date=today,
            status="ABSENT"
        ).count(),

    }


    return render(
        request,
        "reports/dashboard.html",
        context
    )





@login_required
@admin_required
def late_report(request):

    selected_date = request.GET.get("date")

    if selected_date:

        report_date = datetime.strptime(
            selected_date,
            "%Y-%m-%d"
        ).date()

    else:

        report_date = timezone.now().date()



    late_attendance = Attendance.objects.filter(
        attendance_date=report_date,
        status="LATE"
    ).select_related(
        "employee",
        "employee__department"
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

    selected_date = request.GET.get("date")


    if selected_date:

        report_date = datetime.strptime(
            selected_date,
            "%Y-%m-%d"
        ).date()

    else:

        report_date = timezone.now().date()



    absent_attendance = Attendance.objects.filter(
        attendance_date=report_date,
        status="ABSENT"
    ).select_related(
        "employee",
        "employee__department"
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

    selected_date = request.GET.get("date")



    if selected_date:

        report_date = datetime.strptime(
            selected_date,
            "%Y-%m-%d"
        ).date()

    else:

        report_date = timezone.now().date()



    working_hours = Attendance.objects.filter(
        attendance_date=report_date
    ).select_related(
        "employee",
        "employee__department"
    )



    context = {


        "working_hours": working_hours,

        "working_count": working_hours.count(),

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


    selected_date = request.GET.get("date")

    selected_department = request.GET.get(
        "department"
    )



    if selected_date:

        report_date = datetime.strptime(
            selected_date,
            "%Y-%m-%d"
        ).date()

    else:

        report_date = timezone.now().date()



    departments = Department.objects.all()



    attendance_filter = Q(
        attendance__attendance_date=report_date
    )



    department_report = departments.annotate(

        total_employees=Count(
            "employee",
            distinct=True
        ),


        present=Count(
            "employee__attendance",
            filter=Q(
                employee__attendance__attendance_date=report_date,
                employee__attendance__status="PRESENT"
            )
        ),


        late=Count(
            "employee__attendance",
            filter=Q(
                employee__attendance__attendance_date=report_date,
                employee__attendance__status="LATE"
            )
        ),


        half_day=Count(
            "employee__attendance",
            filter=Q(
                employee__attendance__attendance_date=report_date,
                employee__attendance__status="HALF_DAY"
            )
        ),


        absent=Count(
            "employee__attendance",
            filter=Q(
                employee__attendance__attendance_date=report_date,
                employee__attendance__status="ABSENT"
            )
        ),

    )



    if selected_department:

        department_report = department_report.filter(
            id=selected_department
        )



    context = {


        "departments": departments,

        "department_report": department_report,


        "department_count": departments.count(),


        "total_employees": Employee.objects.filter(
            is_active=True
        ).count(),


        "selected_date": report_date,


        "selected_department": selected_department,


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



    present_today = Attendance.objects.filter(
        attendance_date=today,
        status__in=[
            "PRESENT",
            "LATE",
            "HALF_DAY"
        ]
    ).count()



    late_today = Attendance.objects.filter(
        attendance_date=today,
        status="LATE"
    ).count()



    absent_today = Attendance.objects.filter(
        attendance_date=today,
        status="ABSENT"
    ).count()




    department_stats = Department.objects.annotate(

        employee_count=Count(
            "employee",
            filter=Q(
                employee__is_active=True
            )
        )

    )




    context = {


        "total_employees": total_employees,


        "present_today": present_today,


        "late_today": late_today,


        "absent_today": absent_today,


        "department_stats": department_stats,


    }



    return render(
        request,
        "attendance/dashboard_stats.html",
        context
    )