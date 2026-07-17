from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

import secrets
import string

from attendance.decorators import admin_required
from attendance.forms import EmployeeForm
from attendance.models import Department, Employee


def generate_password(length=10):
    """
    Generate a secure random password.
    """

    characters = (
        string.ascii_letters
        + string.digits
        + "@#$%&*"
    )

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


@admin_required
def employee_list(request):

    employees = (
        Employee.objects
        .select_related(
            "department",
            "user",
        )
        .order_by("employee_id")
    )

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    selected_department = request.GET.get(
        "department",
        ""
    )

    selected_status = request.GET.get(
        "status",
        ""
    )

    if search_query:

        employees = employees.filter(

            Q(employee_id__icontains=search_query)

            |

            Q(first_name__icontains=search_query)

            |

            Q(last_name__icontains=search_query)

            |

            Q(email__icontains=search_query)

        )

    if selected_department:

        employees = employees.filter(
            department_id=selected_department
        )

    if selected_status == "active":

        employees = employees.filter(
            is_active=True
        )

    elif selected_status == "inactive":

        employees = employees.filter(
            is_active=False
        )

    paginator = Paginator(
        employees,
        10,
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {

        "page_obj": page_obj,

        "departments": Department.objects.all(),

        "search_query": search_query,

        "selected_department": selected_department,

        "selected_status": selected_status,

    }

    return render(
        request,
        "employee/employee_list.html",
        context,
    )


@admin_required
def employee_detail(request, pk):

    employee = get_object_or_404(

        Employee.objects.select_related(

            "department",

            "user",

        ),

        pk=pk,

    )

    return render(

        request,

        "employee/employee_detail.html",

        {

            "employee": employee,

        },

    )


@admin_required
@transaction.atomic
def employee_create(request):

    if request.method == "POST":

        form = EmployeeForm(
            request.POST
        )

        if form.is_valid():

            employee = form.save(
                commit=False
            )

            employee.save()

            username = employee.employee_id

            password = generate_password()

            try:

                user = User.objects.create_user(

                    username=username,

                    password=password,

                    first_name=employee.first_name,

                    last_name=employee.last_name,

                    email=employee.email,

                    is_active=employee.is_active,

                )

            except Exception as error:

                employee.delete()

                messages.error(

                    request,

                    (
                        "Unable to create login account.\n"
                        f"{error}"
                    ),

                )

                return render(

                    request,

                    "employee/employee_form.html",

                    {

                        "form": form,

                        "title": "Add Employee",

                    },

                )

            employee.user = user

            employee.save(
                update_fields=["user"]
            )

            email_sent = True

            try:

                send_mail(

                    subject="Attendance Management System Login Credentials",

                    message=(

                        f"Hello {employee.first_name},\n\n"

                        "Your employee account has been created successfully.\n\n"

                        f"Employee ID : {employee.employee_id}\n"

                        f"Username : {username}\n"

                        f"Temporary Password : {password}\n\n"

                        "Please login and change your password after first login.\n\n"

                        "Regards,\n"

                        "Administrator"

                    ),

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[employee.email],

                    fail_silently=False,

                )

            except Exception:

                email_sent = False

            if email_sent:

                messages.success(

                    request,

                    (
                        "Employee created successfully.\n"
                        f"Username : {username}\n"
                        f"Temporary Password : {password}\n\n"
                        "Login credentials have been sent to the employee email."
                    ),

                )

            else:

                messages.warning(

                    request,

                    (
                        "Employee created successfully.\n"
                        f"Username : {username}\n"
                        f"Temporary Password : {password}\n\n"
                        "Email could not be sent. Please share the credentials manually."
                    ),

                )

            return redirect(
                "employee_list"
            )

    else:

        form = EmployeeForm()

    return render(

        request,

        "employee/employee_form.html",

        {

            "form": form,

            "title": "Add Employee",

        },

    )


@admin_required
@transaction.atomic
def employee_update(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk,
    )

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            instance=employee,
        )

        if form.is_valid():

            employee = form.save()

            if employee.user:

                employee.user.first_name = employee.first_name
                employee.user.last_name = employee.last_name
                employee.user.email = employee.email
                employee.user.is_active = employee.is_active

                employee.user.save()

            messages.success(
                request,
                "Employee updated successfully.",
            )

            return redirect(
                "employee_list"
            )

    else:

        form = EmployeeForm(
            instance=employee,
        )

    return render(
        request,
        "employee/employee_form.html",
        {
            "form": form,
            "employee": employee,
            "title": "Update Employee",
        },
    )
    
@admin_required
@transaction.atomic
def employee_delete(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk,
    )

    if request.method == "POST":

        if not employee.is_active:

            messages.info(
                request,
                "Employee is already inactive.",
            )

            return redirect(
                "employee_list"
            )

        employee.is_active = False
        employee.save(
            update_fields=["is_active"]
        )

        if employee.user:

            employee.user.is_active = False
            employee.user.save(
                update_fields=["is_active"]
            )

        messages.success(
            request,
            "Employee deactivated successfully.",
        )

        return redirect(
            "employee_list"
        )

    return render(
        request,
        "employee/employee_confirm_delete.html",
        {
            "employee": employee,
        },
    )


@admin_required
@transaction.atomic
def employee_reactivate(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk,
    )

    if request.method == "POST":

        if employee.is_active:

            messages.info(
                request,
                "Employee is already active.",
            )

            return redirect(
                "employee_list"
            )

        employee.is_active = True
        employee.save(
            update_fields=["is_active"]
        )

        if employee.user:

            employee.user.is_active = True
            employee.user.save(
                update_fields=["is_active"]
            )

        messages.success(
            request,
            "Employee reactivated successfully.",
        )

        return redirect(
            "employee_list"
        )

    return render(
        request,
        "employee/employee_confirm_reactivate.html",
        {
            "employee": employee,
        },
    )