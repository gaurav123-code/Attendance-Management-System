from django.urls import path

from .views import (
    admin_views,
    attendance_views,
    auth_views,
    employee_views,
    export_views,
    report_views,
)

urlpatterns = [

    # ==========================================================
    # Dashboard
    # ==========================================================

    path(
        "dashboard/",
        attendance_views.dashboard,
        name="dashboard",
    ),

    path(
        "admin-dashboard/",
        admin_views.admin_dashboard,
        name="admin_dashboard",
    ),

    # ==========================================================
    # Authentication
    # ==========================================================

    path(
        "change-password/",
        auth_views.change_password,
        name="change_password",
    ),

    # ==========================================================
    # Employee Management
    # ==========================================================

    path(
        "employees/",
        employee_views.employee_list,
        name="employee_list",
    ),

    path(
        "employees/inactive/",
        employee_views.inactive_employee_list,
        name="inactive_employee_list",
    ),

    path(
        "employees/create/",
        employee_views.employee_create,
        name="employee_create",
    ),

    path(
        "employees/<int:id>/",
        employee_views.employee_detail,
        name="employee_detail",
    ),

    path(
        "employees/<int:id>/edit/",
        employee_views.employee_update,
        name="employee_update",
    ),

    path(
        "employees/<int:id>/delete/",
        employee_views.employee_delete,
        name="employee_delete",
    ),

    path(
        "employees/<int:id>/reactivate/",
        employee_views.employee_reactivate,
        name="employee_reactivate",
    ),

    # ==========================================================
    # Attendance
    # ==========================================================

    path(
        "attendance/check-in/",
        attendance_views.check_in,
        name="check_in",
    ),

    path(
        "attendance/check-out/",
        attendance_views.check_out,
        name="check_out",
    ),

    path(
        "attendance/my/",
        attendance_views.my_attendance,
        name="my_attendance",
    ),

    path(
        "attendance/list/",
        attendance_views.attendance_list,
        name="attendance_list",
    ),

    path(
        "attendance/manage/",
        attendance_views.attendance_manage,
        name="attendance_manage",
    ),

    path(
        "attendance/mark/",
        attendance_views.mark_attendance,
        name="mark_attendance",
    ),

    path(
        "attendance/absent-mark/",
        attendance_views.absent_mark,
        name="absent_mark",
    ),

    path(
        "attendance/<int:id>/",
        attendance_views.attendance_detail,
        name="attendance_detail",
    ),

    # ==========================================================
    # Reports
    # ==========================================================

    path(
        "reports/",
        report_views.report_dashboard,
        name="report_dashboard",
    ),

    path(
        "reports/late/",
        report_views.late_report,
        name="late_report",
    ),

    path(
        "reports/absent/",
        report_views.absent_report,
        name="absent_report",
    ),

    path(
        "reports/working-hours/",
        report_views.working_hours_report,
        name="working_hours_report",
    ),

    path(
        "reports/department/",
        report_views.department_attendance_report,
        name="department_attendance_report",
    ),

    path(
        "reports/dashboard-stats/",
        report_views.dashboard_stats,
        name="dashboard_stats",
    ),

    # ==========================================================
    # Export Reports
    # ==========================================================

    path(
        "reports/export/",
        export_views.export_report,
        name="export_report",
    ),
    
    path(
    "employees/<int:id>/reset-password/",
    employee_views.admin_reset_password,
    name="admin_reset_password",
    ),
    
    path(
    "reports/export-page/",
    export_views.export_page,
    name="export_page",
    ),
    
]