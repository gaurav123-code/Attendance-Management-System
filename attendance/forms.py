from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import (
    Employee,
    Department,
    Attendance,
)


# ==========================
# Employee Form
# ==========================

class EmployeeForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
        required=False
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
        required=False
    )


    class Meta:

        model = Employee

        fields = [

            "first_name",
            "last_name",
            "email",
            "phone_number",
            "department",
            "date_joined",
            "is_active",

        ]


        widgets = {

            "date_joined": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First Name"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number"
                }
            ),

            "department": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

        }



    def clean_email(self):

        email = self.cleaned_data.get(
            "email"
        )

        if Employee.objects.filter(
            email=email
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "Email already exists."
            )


        return email



    def clean(self):

        cleaned_data = super().clean()


        password = cleaned_data.get(
            "password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )


        if password or confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )


        return cleaned_data



# ==========================
# Change Password Form
# ==========================

class CustomPasswordChangeForm(
    PasswordChangeForm
):


    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Old Password"
            }
        )
    )


    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter New Password"
            }
        )
    )


    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm New Password"
            }
        )
    )



# ==========================
# Attendance Form
# ==========================

class AttendanceForm(forms.ModelForm):


    class Meta:

        model = Attendance


        fields = [

            "employee",
            "attendance_date",
            "status",
            "check_in",
            "check_out",
            "remarks",

        ]


        widgets = {


            "attendance_date": forms.DateInput(

                attrs={
                    "type": "date",
                    "class": "form-control"
                }

            ),


            "employee": forms.Select(

                attrs={
                    "class": "form-select"
                }

            ),


            "status": forms.Select(

                attrs={
                    "class": "form-select"
                }

            ),


            "check_in": forms.TimeInput(

                attrs={
                    "type": "time",
                    "class": "form-control"
                }

            ),


            "check_out": forms.TimeInput(

                attrs={
                    "type": "time",
                    "class": "form-control"
                }

            ),


            "remarks": forms.Textarea(

                attrs={
                    "class": "form-control",
                    "rows": 3
                }

            ),

        }



    def clean(self):

        cleaned_data = super().clean()


        check_in = cleaned_data.get(
            "check_in"
        )

        check_out = cleaned_data.get(
            "check_out"
        )


        if check_in and check_out:

            if check_out <= check_in:

                raise forms.ValidationError(
                    "Check out time must be after check in time."
                )


        return cleaned_data



# ==========================
# Department Form
# ==========================

class DepartmentForm(forms.ModelForm):


    class Meta:

        model = Department


        fields = [

            "name",
            "description",

        ]


        widgets = {


            "name": forms.TextInput(

                attrs={
                    "class": "form-control"
                }

            ),


            "description": forms.Textarea(

                attrs={
                    "class": "form-control",
                    "rows": 3
                }

            ),

        }