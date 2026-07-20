from django.core.management.base import BaseCommand
from django.utils import timezone

from attendance.models import Attendance, Employee


class Command(BaseCommand):
    help = "Automatically mark absent employees after office cutoff time"


    def handle(self, *args, **options):

        today = timezone.localdate()


        employees = Employee.objects.filter(
            is_active=True
        )


        created_count = 0


        for employee in employees:

            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                attendance_date=today,
                defaults={
                    "status": Attendance.ABSENT,
                    "remarks": "Automatically marked absent"
                }
            )


            if created:
                created_count += 1


        self.stdout.write(
            self.style.SUCCESS(
                f"{created_count} employees marked absent successfully."
            )
        )