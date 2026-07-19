from datetime import datetime, time

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        unique=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees"
    )

    date_joined = models.DateField()

    is_active = models.BooleanField(default=True)

    must_change_password = models.BooleanField(
        default=True
    )

    password_changed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    password_reset_token = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    password_reset_token_expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = Employee.objects.order_by(
                "-id"
            ).first()

            if last_employee:
                last_number = int(
                    last_employee.employee_id.replace(
                        "EMP",
                        ""
                    )
                )
                new_number = last_number + 1
            else:
                new_number = 1

            self.employee_id = f"EMP{new_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):

    PRESENT = "PRESENT"
    LATE = "LATE"
    HALF_DAY = "HALF_DAY"
    ABSENT = "ABSENT"

    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (LATE, "Late"),
        (HALF_DAY, "Half Day"),
        (ABSENT, "Absent"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    attendance_date = models.DateField(
        default=timezone.now
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ABSENT
    )

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    working_hours = models.DurationField(
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def calculate_status(self):
        if not self.check_in:
            return self.status

        late_time = time(9, 45)
        half_day_time = time(13, 30)

        if self.check_in >= half_day_time:
            return self.HALF_DAY

        if self.check_in >= late_time:
            return self.LATE

        return self.PRESENT
    
    def calculate_working_hours(self):
        if self.check_in and self.check_out:
            check_in_datetime = datetime.combine(
                self.attendance_date,
                self.check_in
            )

            check_out_datetime = datetime.combine(
                self.attendance_date,
                self.check_out
            )

            return check_out_datetime - check_in_datetime

        return None

    def save(self, *args, **kwargs):

        if self.check_in:
            self.status = self.calculate_status()

        self.working_hours = self.calculate_working_hours()

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.employee} - "
            f"{self.attendance_date}"
        )