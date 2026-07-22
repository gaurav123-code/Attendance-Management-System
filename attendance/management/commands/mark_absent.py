from django.core.management.base import BaseCommand
from django.utils import timezone

from attendance.models import Attendance, Employee


class Command(BaseCommand):

    help = "Automatically mark absent employees after 3 PM cutoff time"


    def handle(self, *args, **options):

        today = timezone.localdate()

        current_time = timezone.localtime().time()


        # Absent marking allowed after 3 PM only
        if current_time < timezone.datetime.strptime(
            "15:00",
            "%H:%M"
        ).time():

            self.stdout.write(
                self.style.WARNING(
                    "Absent can be marked only after 3:00 PM."
                )
            )

            return



        employees = Employee.objects.filter(
            is_active=True
        )


        created_count = 0


        for employee in employees:


            attendance = Attendance.objects.filter(
                employee=employee,
                attendance_date=today
            ).first()



            # Already checked in
            if attendance and attendance.check_in:

                continue



            # No check-in or no attendance record
            if attendance:

                attendance.status = Attendance.ABSENT

                attendance.remarks = (
                    "Automatically marked absent "
                    "due to no check-in before cutoff time."
                )

                attendance.save()



            else:

                Attendance.objects.create(

                    employee=employee,

                    attendance_date=today,

                    status=Attendance.ABSENT,

                    remarks=(
                        "Automatically marked absent "
                        "due to no check-in before cutoff time."
                    )

                )


            created_count += 1



        self.stdout.write(

            self.style.SUCCESS(

                f"{created_count} employees marked absent successfully."

            )

        )