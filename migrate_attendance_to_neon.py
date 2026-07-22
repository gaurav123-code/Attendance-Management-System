import os
import django
import json
from datetime import datetime


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "attendance_system.settings"
)

django.setup()


from attendance.models import Attendance, Employee


BACKUP_FILE = "attendance_backup.json"


def format_time(value):
    if not value:
        return None

    return datetime.strptime(
        value[:5],
        "%H:%M"
    ).time()



def format_date(value):

    return datetime.strptime(
        value,
        "%Y-%m-%d"
    ).date()



def format_datetime(value):

    if not value:
        return None

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )



LOCAL_EMPLOYEE_MAP = {
    1: "EMP0001",
    2: "EMP0002",
    4: "EMP0003",
    5: "EMP0004",
    6: "EMP0005",
    7: "EMP0006",
    8: "EMP0008",
    9: "EMP0009",
    10: "EMP0010",
}



def migrate_attendance():

    with open(BACKUP_FILE, "r") as file:
        data = json.load(file)


    created = 0
    skipped = 0


    for item in data:

        fields = item["fields"]


        employee_code = LOCAL_EMPLOYEE_MAP.get(
            fields["employee"]
        )


        if not employee_code:
            skipped += 1
            continue



        try:

            employee = Employee.objects.get(
                employee_id=employee_code
            )

        except Employee.DoesNotExist:

            print(
                f"Employee missing: {employee_code}"
            )

            skipped += 1
            continue



        exists = Attendance.objects.filter(
            employee=employee,
            attendance_date=format_date(
                fields["attendance_date"]
            )
        ).exists()


        if exists:

            print(
                f"Skipped duplicate: {employee_code} "
                f"{fields['attendance_date']}"
            )

            skipped += 1
            continue



        attendance = Attendance(
            employee=employee,
            attendance_date=format_date(
                fields["attendance_date"]
            ),
            status=fields["status"],
            check_in=format_time(
                fields["check_in"]
            ),
            check_out=format_time(
                fields["check_out"]
            ),
            remarks=fields["remarks"],
            created_at=format_datetime(
                fields["created_at"]
            ),
            updated_at=format_datetime(
                fields["updated_at"]
            ),
        )


        original_status = fields["status"]


        attendance.save()


        Attendance.objects.filter(
            id=attendance.id
        ).update(
            status=original_status
        )


        created += 1


        print(
            f"Created: {employee_code} "
            f"{fields['attendance_date']}"
        )


    print("\nMigration Completed")
    print("Created:", created)
    print("Skipped:", skipped)



if __name__ == "__main__":
    migrate_attendance()