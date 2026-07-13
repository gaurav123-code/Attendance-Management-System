from django.contrib import admin

from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    readonly_fields = (
        "employee_id",
        "created_at",
        "updated_at",
    )

    list_display = (
        "employee_id",
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

    ordering = ("employee_id",)

    list_select_related = ("department",)

    list_per_page = 20