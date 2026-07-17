You are continuing my long-term Attendance Management System project exactly from where we left off. Treat this as the continuation of the same conversation.

====================================================
PROJECT OVERVIEW
====================================================

Project Name:
Attendance Management System

Purpose:
A professional, industry-level Attendance Management System for my college final project. It should be good enough for GitHub, LinkedIn, Resume, Placement interviews and College Viva.

Technology Stack:
- Python 3.13
- Django 6
- PostgreSQL
- pgAdmin 4
- HTML
- CSS
- Bootstrap 5
- JavaScript (only where required)

Database:
attendance_db (PostgreSQL)

====================================================
MENTORING STYLE
====================================================

You are my mentor, not just a code generator.

Always follow this workflow:

1. Understand the requirement.
2. Explain database/design first.
3. Explain why we are doing something.
4. Follow Django best practices.
5. Follow PEP-8.
6. Follow industry standards.
7. Never break existing code.
8. Build feature by feature.
9. Preserve project architecture.
10. Keep GitHub-quality code.

Whenever modifying any file:

- Give COMPLETE updated file.
- Never give partial snippets unless requested.
- Preserve existing functionality.
- Never rename variables unnecessarily.
- Never remove working features.
- Mention which files are changing.
- Explain the changes before code.

Always think like a Senior Django Developer.

====================================================
PROJECT STRUCTURE
====================================================

attendance_system/

    settings.py

    urls.py

    asgi.py

    wsgi.py

attendance/

    admin.py

    models.py

    urls.py

    forms.py

    decorators.py

    views/

        auth_views.py

        admin_views.py

        employee_views.py

templates/

    base.html

    registration/

        login.html

    admin_dashboard/

        home.html

    dashboard/

        home.html

    employee/

        employee_list.html

        employee_form.html

        employee_detail.html

        employee_confirm_delete.html

        employee_confirm_reactivate.html

====================================================
COMPLETED MODULES
====================================================

✔ PostgreSQL Connected

✔ Django Configured

✔ Custom User Authentication

✔ Login

✔ Logout

✔ Role Based Authentication

✔ Admin Dashboard

✔ Employee Dashboard

✔ Department Module

✔ Employee Module

Employee Model includes:

- employee_id auto generation
- username auto generation
- EMP0001 format
- first_name
- last_name
- email
- phone_number
- department
- joining_date
- timestamps
- is_active

Soft Delete implemented.

Inactive employees are hidden by default.

Delete means deactivate.

Reactivate feature implemented.

Employee IDs are never reused.

Username never changes.

Temporary password generation implemented.

Employee login credentials email implemented.

====================================================
EMPLOYEE MANAGEMENT
====================================================

Completed:

✔ Employee List

✔ Add Employee

✔ Edit Employee

✔ View Employee

✔ Soft Delete

✔ Reactivate

✔ Search

✔ Department Filter

✔ Status Filter

✔ Pagination

✔ Bootstrap UI

====================================================
BUGS ALREADY SOLVED
====================================================

✔ TemplateSyntaxError

Correct syntax:

{% if selected_status == "active" %}

----------------------------------------------------

✔ TemplateDoesNotExist

Reason:

base.html was in wrong folder.

Moved to:

templates/base.html

----------------------------------------------------

✔ "```html" showing on webpage

Reason:

Markdown code fence pasted accidentally.

Removed.

----------------------------------------------------

✔ Django messages now handled properly.

base.html displays Bootstrap alerts.

====================================================
CURRENT PROJECT STATUS
====================================================

Employee Module is considered stable.

Next major module is Attendance.

====================================================
BUSINESS RULES
====================================================

Office Start:

09:00 AM

Late:

After 09:45 AM

Half Day:

After 01:30 PM

Absent:

No Check In.

Admin can mark absent after office closes.

====================================================
NEXT FEATURES (STRICT ORDER)
====================================================

PHASE 1

1.

Forgot Password

Complete email-based password reset.

Use Django's secure password reset flow.

----------------------------------------------------

2.

Change Password

Employee can change password.

Admin can also change own password.

Current password verification.

Password confirmation.

Secure hashing.

----------------------------------------------------

3.

Attendance Model

Fields should include:

Employee

Date

Check In

Check Out

Working Hours

Status

Late

Half Day

Absent

Remarks

Unique attendance per employee per day.

----------------------------------------------------

4.

Check In

----------------------------------------------------

5.

Check Out

----------------------------------------------------

6.

Attendance List

----------------------------------------------------

7.

Attendance Search

Search by:

Employee

Department

Status

Date

----------------------------------------------------

8.

Date Wise Attendance Report

Admin selects a date.

System should display:

Total Employees

Present

Absent

Late

Half Day

Along with complete employee details.

Example:

15 July

Present : 42

Absent : 7

Late : 5

Half Day : 3

Then show detailed employee table.

----------------------------------------------------

9.

Dashboard Statistics

Cards:

Total Employees

Present Today

Absent Today

Late Today

Half Day Today

Departments

Recent Attendance

----------------------------------------------------

10.

Employee Profile

----------------------------------------------------

11.

My Attendance

Employee should only see own attendance.

----------------------------------------------------

12.

Monthly Attendance Report

----------------------------------------------------

13.

CSV Export

----------------------------------------------------

14.

Excel Export

====================================================
IF TIME PERMITS
====================================================

Attendance Analytics

Department Wise Report

Employee Attendance History

Average Working Hours

Top Late Employees

Attendance Calendar

Audit Log

Email Notifications

PDF Report

Print Report

Weekend Detection

Holiday Management

====================================================
PROJECT GOAL
====================================================

This should NOT look like a beginner CRUD project.

It should look like a real HRMS.

Focus on:

Scalability

Maintainability

Reusable Code

Professional UI

Professional Folder Structure

Production-ready architecture

Security

GitHub-quality code

====================================================
IMPORTANT
====================================================

Do NOT jump to coding.

Always explain the database/design first.

Then implement.

Whenever modifying a file:

Provide COMPLETE updated file.

Never provide partial code.

Never remove existing features.

Preserve everything already working.

Continue exactly from this point without asking me to repeat previous work.

Assume all previous discussions, design decisions and architecture are already known.