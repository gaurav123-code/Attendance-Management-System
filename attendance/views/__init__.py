from .attendance_views import (
    dashboard,
    check_in,
    check_out,
    attendance_list,
)

from .admin_views import (
    admin_dashboard,
)

from .employee_views import (
    employee_list,
    employee_detail,
    employee_create,
    employee_update,
    employee_delete,
    employee_reactivate,
)

from .auth_views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    CustomPasswordChangeView,
)

from .report_views import (
    report_dashboard,
)

from .export_views import (
    export_attendance_csv,
    export_attendance_excel,
)


__all__ = [

    # Attendance

    "dashboard",
    "check_in",
    "check_out",
    "attendance_list",


    # Admin

    "admin_dashboard",


    # Employee

    "employee_list",
    "employee_detail",
    "employee_create",
    "employee_update",
    "employee_delete",
    "employee_reactivate",


    # Authentication

    "CustomLoginView",
    "CustomLogoutView",
    "CustomPasswordResetView",
    "CustomPasswordResetDoneView",
    "CustomPasswordResetConfirmView",
    "CustomPasswordResetCompleteView",
    "CustomPasswordChangeView",


    # Reports

    "report_dashboard",


    # Export

    "export_attendance_csv",
    "export_attendance_excel",

]