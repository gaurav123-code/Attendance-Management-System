from .attendance_views import (
    dashboard,
    check_in,
    check_out,
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
)

__all__ = [
    "dashboard",
    "check_in",
    "check_out",
    "admin_dashboard",
    "employee_list",
    "employee_detail",
    "employee_create",
    "employee_update",
    "employee_delete",
]