import secrets
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..decorators import admin_required
from ..forms import (
    EmployeeForm,
    AdminResetPasswordForm,
)
from ..models import Attendance, Employee, Department



# ==========================
# Generate Temporary Password
# ==========================

def generate_password(length=10):

    characters = (
        string.ascii_letters
        + string.digits
        + "@#$%"
    )

    return "".join(

        secrets.choice(characters)

        for _ in range(length)

    )





# ==========================
# Generate Employee ID
# ==========================

def generate_employee_id():

    last_employee = Employee.objects.order_by(
        "-id"
    ).first()



    if last_employee:

        number = last_employee.id + 1

    else:

        number = 1



    return f"EMP{number:04d}"







# ==========================
# Active Employee List
# ==========================

@admin_required
def employee_list(request):

    employees = Employee.objects.select_related(

        "department",

        "user"

    ).filter(

        is_active=True

    )



    search = request.GET.get(
        "search"
    )


    department = request.GET.get(
        "department"
    )



    if search:


        employees = employees.filter(


            Q(employee_id__icontains=search)

            |

            Q(first_name__icontains=search)

            |

            Q(last_name__icontains=search)

            |

            Q(email__icontains=search)


        )





    if department:


        employees = employees.filter(

            department_id=department

        )





    paginator = Paginator(

        employees,

        10

    )



    page_number = request.GET.get(

        "page"

    )



    page_obj = paginator.get_page(

        page_number

    )



    context = {


        "employees": page_obj,
        
        "departments": Department.objects.all(),


    }



    return render(

        request,

        "employee/employee_list.html",

        context

    )









# ==========================
# Inactive Employee List
# ==========================

@admin_required
def inactive_employee_list(request):


    employees = Employee.objects.select_related(

        "department",

        "user"

    ).filter(

        is_active=False

    )



    search = request.GET.get(

        "search"

    )


    department = request.GET.get(

        "department"

    )





    if search:


        employees = employees.filter(


            Q(employee_id__icontains=search)

            |

            Q(first_name__icontains=search)

            |

            Q(last_name__icontains=search)

            |

            Q(email__icontains=search)


        )





    if department:


        employees = employees.filter(

            department_id=department

        )





    paginator = Paginator(

        employees,

        10

    )


    page_number = request.GET.get(

        "page"

    )



    page_obj = paginator.get_page(

        page_number

    )




    context = {


        "employees": page_obj,


    }



    return render(

        request,

        "employee/inactive_employee_list.html",

        context

    )









# ==========================
# Create Employee
# ==========================

@admin_required
def employee_create(request):


    if request.method == "POST":



        form = EmployeeForm(

            request.POST

        )



        if form.is_valid():



            password = form.cleaned_data.get(

                "password"

            )



            if not password:


                password = generate_password()





            employee = form.save(

                commit=False

            )



            employee.employee_id = generate_employee_id()



            employee.must_change_password = True





            user = User.objects.create_user(


                username=employee.employee_id,


                password=password,


                email=employee.email,


                first_name=employee.first_name,


                last_name=employee.last_name


            )



            employee.user = user



            employee.save()



            send_mail(


                subject="Your HRMS Account Created",



                message=f"""
Hello {employee.first_name},


Your employee account has been created successfully.


Employee Name:
{employee.first_name} {employee.last_name}


Employee ID (Login ID):
{employee.employee_id}


Temporary Password:
{password}


Please login using your Employee ID and change your password after first login.


Regards,

HR Department
""",



                from_email=settings.EMAIL_HOST_USER,



                recipient_list=[

                    employee.email

                ],



                fail_silently=False,


            )



            messages.success(


                request,


                "Employee created successfully. Login credentials sent to employee email."


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

            "form": form

        }

    )






# ==========================
# Employee Detail
# ==========================

@admin_required
def employee_detail(request, id):


    employee = get_object_or_404(

        Employee,

        id=id

    )



    attendance_records = (

        Attendance.objects

        .filter(

            employee=employee

        )

        .order_by(

            "-attendance_date"

        )

    )



    total_attendance = attendance_records.count()



    present_count = attendance_records.filter(

        status="PRESENT"

    ).count()



    late_count = attendance_records.filter(

        status="LATE"

    ).count()



    half_day_count = attendance_records.filter(

        status="HALF_DAY"

    ).count()



    absent_count = attendance_records.filter(

        status="ABSENT"

    ).count()




    context = {


        "employee": employee,


        "attendance_records": attendance_records,


        "total_attendance": total_attendance,


        "present_count": present_count,


        "late_count": late_count,


        "half_day_count": half_day_count,


        "absent_count": absent_count,


    }



    return render(

        request,

        "employee/employee_detail.html",

        context

    )









# ==========================
# Update Employee
# ==========================

@admin_required
def employee_update(request, id):


    employee = get_object_or_404(

        Employee,

        id=id

    )



    if request.method == "POST":



        form = EmployeeForm(

            request.POST,

            instance=employee

        )



        if form.is_valid():



            employee = form.save()



            if employee.user:



                employee.user.first_name = (

                    employee.first_name

                )


                employee.user.last_name = (

                    employee.last_name

                )


                employee.user.email = (

                    employee.email

                )


                employee.user.save()




            messages.success(


                request,


                "Employee updated successfully."


            )



            return redirect(

                "employee_detail",

                employee.id

            )



    else:



        form = EmployeeForm(

            instance=employee

        )



    return render(

        request,

        "employee/employee_form.html",

        {


            "form": form,


            "employee": employee


        }

    )









# ==========================
# Deactivate Employee
# ==========================

@admin_required
def employee_delete(request, id):


    employee = get_object_or_404(

        Employee,

        id=id

    )



    employee.is_active = False



    employee.save()



    if employee.user:



        employee.user.is_active = False


        employee.user.save()




    messages.success(


        request,


        "Employee deactivated successfully."


    )



    return redirect(

        "employee_list"

    )

@admin_required
def inactive_employee_list(request):

    employees = Employee.objects.select_related(
        "department",
        "user"
    ).filter(
        is_active=False
    )


    search = request.GET.get(
        "search"
    )


    department = request.GET.get(
        "department"
    )



    if search:

        employees = employees.filter(

            Q(employee_id__icontains=search)

            |

            Q(first_name__icontains=search)

            |

            Q(last_name__icontains=search)

            |

            Q(email__icontains=search)

        )



    if department:

        employees = employees.filter(

            department_id=department

        )



    paginator = Paginator(

        employees,

        10

    )


    page_number = request.GET.get(
        "page"
    )


    page_obj = paginator.get_page(
        page_number
    )



    context = {


        "employees": page_obj,


        "departments": Department.objects.all(),


    }



    return render(

        request,

        "employee/inactive_employee_list.html",

        context

    )







# ==========================
# Reactivate Employee
# ==========================

@admin_required
def employee_reactivate(request, id):


    employee = get_object_or_404(

        Employee,

        id=id

    )



    employee.is_active = True



    employee.save()



    if employee.user:



        employee.user.is_active = True


        employee.user.save()




    messages.success(


        request,


        "Employee reactivated successfully."


    )



    return redirect(

        "employee_list"

    )

@admin_required
def admin_reset_password(request, id):

    employee = get_object_or_404(
        Employee,
        id=id
    )

    if not employee.user:

        messages.error(
            request,
            "Employee login account not found."
        )

        return redirect(
            "employee_detail",
            id=employee.id
        )

    if request.method == "POST":

        form = AdminResetPasswordForm(
            employee.user,
            request.POST
        )

        if form.is_valid():

            form.save()

            employee.must_change_password = True

            employee.save()

            messages.success(
                request,
                "Password reset successfully."
            )

            return redirect(
                "employee_detail",
                id=employee.id
            )

    else:

        form = AdminResetPasswordForm(
            employee.user
        )

    context = {

        "employee": employee,

        "form": form,

    }

    return render(

        request,

        "employee/admin_reset_password.html",

        context,

    )