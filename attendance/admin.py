from django.contrib import admin

from .models import Attendance, Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    readonly_fields = (
        "employee_id",
        "created_at",
        "updated_at",
    )

    fields = (
        "user",
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "department",
        "date_joined",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_display = (
        "employee_id",
        "user",
        "first_name",
        "last_name",
        "email",
        "department",
        "is_active",
        "created_at",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "last_name",
        "email",
    )

    list_filter = (
        "department",
        "is_active",
        "date_joined",
    )

    ordering = (
        "employee_id",
    )

    list_select_related = (
        "department",
        "user",
    )

    list_per_page = 20


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    readonly_fields = (
        "working_hours",
        "created_at",
        "updated_at",
    )

    list_display = (
        "employee_id_display",
        "employee_name",
        "attendance_date",
        "status",
        "check_in",
        "check_out",
        "working_hours",
    )

    search_fields = (
        "employee__employee_id",
        "employee__first_name",
        "employee__last_name",
        "employee__email",
    )

    list_filter = (
        "status",
        "attendance_date",
        "employee__department",
    )

    date_hierarchy = "attendance_date"

    list_select_related = (
        "employee",
        "employee__department",
    )

    autocomplete_fields = (
        "employee",
    )

    ordering = (
        "-attendance_date",
        "employee",
    )

    list_per_page = 20

    @admin.display(
        ordering="employee__employee_id",
        description="Employee ID",
    )
    def employee_id_display(self, obj):
        return obj.employee.employee_id

    @admin.display(
        ordering="employee__first_name",
        description="Employee Name",
    )
    def employee_name(self, obj):
        return obj.employee.full_name