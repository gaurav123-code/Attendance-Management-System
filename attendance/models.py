from django.db import models
from django.core.exceptions import ValidationError
from datetime import time
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="employee",
    null=True,
    blank=True,
)
    employee_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )

    first_name = models.CharField(
        max_length=50
    )

    last_name = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=15
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees"
    )

    date_joined = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = Employee.objects.order_by("-id").first()

            if last_employee:
                last_id = int(last_employee.employee_id[3:])
                new_id = last_id + 1
            else:
                new_id = 1

            self.employee_id = f"EMP{new_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

class Attendance(models.Model):

    OFFICE_START_TIME = time(9, 0)
    LATE_AFTER = time(9, 45)
    HALF_DAY_AFTER = time(13, 30)

    class AttendanceStatus(models.TextChoices):
        PRESENT = "P", "Present"
        ABSENT = "A", "Absent"
        LATE = "L", "Late"
        HALF_DAY = "H", "Half Day"
        LEAVE = "LV", "Leave"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="attendances"
    )

    attendance_date = models.DateField(
        db_index=True
    )

    status = models.CharField(
    max_length=2,
    choices=AttendanceStatus.choices,
    default=AttendanceStatus.ABSENT,
    )
    
    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
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

    class Meta:
        ordering = ("-attendance_date", "employee")

        constraints = [
            models.UniqueConstraint(
                fields=["employee", "attendance_date"],
                name="unique_employee_attendance"
            )
        ]

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.attendance_date} - "
            f"{self.get_status_display()}"
        )

    def clean(self):
        super().clean()

        self._validate_status()
        self._validate_check_times()

    def save(self, *args, **kwargs):
        self._calculate_status()
        self.full_clean()

        super().save(*args, **kwargs)

    def _calculate_status(self):
        if not self.check_in:
            return

        if self.check_in <= self.LATE_AFTER:
            self.status = self.AttendanceStatus.PRESENT

        elif self.check_in <= self.HALF_DAY_AFTER:
            self.status = self.AttendanceStatus.LATE

        else:
            self.status = self.AttendanceStatus.HALF_DAY

    def _validate_status(self):
        if self.check_in:
            return

        if self.status not in {
            self.AttendanceStatus.ABSENT,
            self.AttendanceStatus.LEAVE,
        }:
            raise ValidationError(
                {
                    "status": (
                        "Select either Absent or Leave when "
                        "no check-in time is provided."
                    )
                }
            )

        if self.check_out:
            raise ValidationError(
                {
                    "check_out": (
                        "Check-out time cannot be provided "
                        "without a check-in time."
                    )
                }
            )

    def _validate_check_times(self):
        if self.check_in and self.check_out:
            if self.check_out <= self.check_in:
                raise ValidationError(
                    {
                        "check_out": (
                            "Check-out time must be later than "
                            "check-in time."
                        )
                    }
                )