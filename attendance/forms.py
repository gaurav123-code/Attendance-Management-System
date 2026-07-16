from django import forms
from django.core.exceptions import ValidationError

from attendance.models import Employee


class EmployeeForm(forms.ModelForm):
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
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        queryset = Employee.objects.filter(
            email=email
        )

        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise ValidationError(
                "Employee with this email already exists."
            )

        return email

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"].strip()

        if not phone.isdigit():
            raise ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 10:
            raise ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return phone

    def clean_first_name(self):
        return self.cleaned_data["first_name"].strip().title()

    def clean_last_name(self):
        return self.cleaned_data["last_name"].strip().title()