from django.contrib import admin

from .models import (
    Department,
    Employee,
    Attendance,
)





@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):


    list_display = [

        "id",

        "name",

        "created_at",

        "updated_at",

    ]


    search_fields = [

        "name",

    ]






@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):


    list_display = [

        "employee_id",

        "first_name",

        "last_name",

        "email",

        "department",

        "is_active",

        "created_at",

    ]



    list_filter = [

        "department",

        "is_active",

    ]



    search_fields = [

        "employee_id",

        "first_name",

        "last_name",

        "email",

    ]



    readonly_fields = [

        "employee_id",

        "created_at",

        "updated_at",

    ]







@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):


    list_display = [

        "employee",

        "attendance_date",

        "status",

        "check_in",

        "check_out",

        "working_hours",

    ]



    list_filter = [

        "status",

        "attendance_date",

    ]



    search_fields = [

        "employee__employee_id",

        "employee__first_name",

        "employee__last_name",

    ]



    readonly_fields = [

        "working_hours",

        "created_at",

        "updated_at",

    ]



    date_hierarchy = "attendance_date"