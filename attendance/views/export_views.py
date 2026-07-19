import csv

import openpyxl

from django.http import HttpResponse

from ..decorators import admin_required
from ..models import Attendance



# ==========================
# Export Attendance CSV
# ==========================

@admin_required
def export_attendance_csv(request):

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="attendance_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Employee ID",
        "Employee Name",
        "Department",
        "Date",
        "Status",
        "Check In",
        "Check Out",
        "Working Hours"
    ])

    attendance_records = Attendance.objects.select_related(
        "employee",
        "employee__department"
    ).all()


    for attendance in attendance_records:

        writer.writerow([

            attendance.employee.employee_id,

            (
                attendance.employee.first_name
                +
                " "
                +
                attendance.employee.last_name
            ),

            attendance.employee.department.name,

            attendance.attendance_date,

            attendance.status,

            attendance.check_in,

            attendance.check_out,

            attendance.working_hours,

        ])


    return response





# ==========================
# Export Attendance Excel
# ==========================

@admin_required
def export_attendance_excel(request):

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Attendance Report"


    sheet.append([

        "Employee ID",
        "Employee Name",
        "Department",
        "Date",
        "Status",
        "Check In",
        "Check Out",
        "Working Hours"

    ])



    attendance_records = Attendance.objects.select_related(

        "employee",
        "employee__department"

    ).all()



    for attendance in attendance_records:

        sheet.append([

            attendance.employee.employee_id,

            (
                attendance.employee.first_name
                +
                " "
                +
                attendance.employee.last_name
            ),

            attendance.employee.department.name,

            str(attendance.attendance_date),

            attendance.status,

            str(attendance.check_in),

            str(attendance.check_out),

            str(attendance.working_hours),

        ])




    response = HttpResponse(

        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )


    response["Content-Disposition"] = (

        'attachment; filename="attendance_report.xlsx"'

    )



    workbook.save(response)


    return response





# ==========================
# Export Report Wrapper
# ==========================

@admin_required
def export_report(request):

    return export_attendance_excel(request)