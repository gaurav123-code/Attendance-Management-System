from django.urls import path

from attendance import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),

    path(
        "check-in/",
        views.check_in,
        name="check_in",
    ),

    path(
        "check-out/",
        views.check_out,
        name="check_out",
    ),


    # Employee Management

    path(
        "employees/",
        views.employee_list,
        name="employee_list",
    ),

    path(
        "employees/create/",
        views.employee_create,
        name="employee_create",
    ),

    path(
        "employees/<int:pk>/",
        views.employee_detail,
        name="employee_detail",
    ),

    path(
        "employees/<int:pk>/edit/",
        views.employee_update,
        name="employee_update",
    ),

    path(
        "employees/<int:pk>/delete/",
        views.employee_delete,
        name="employee_delete",
    ),

    path(
        "employees/<int:pk>/reactivate/",
        views.employee_reactivate,
        name="employee_reactivate",
    ),

]