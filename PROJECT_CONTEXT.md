# Attendance Management System (Continuation Prompt)

Hi ChatGPT,

This is a continuation of my Attendance Management System project. Treat everything below as the complete project context and continue from this exact stage without repeating previous setup or asking for already completed steps.

==================================================
PROJECT INFORMATION
===================

Project Name:
Attendance Management System for Employees

Purpose:
This project is assigned by my college.

The final project should be professional enough to showcase on:

* GitHub
* LinkedIn
* Resume
* Portfolio

Do NOT build it like a beginner CRUD project.

Build it like a real company-level application while teaching me every concept.

==================================================
TECH STACK
==========

Backend

* Python
* Django 6.x

Database

* PostgreSQL 17
* pgAdmin 4

Frontend

* HTML
* CSS
* JavaScript (later if required)
* Bootstrap (later if required)

==================================================
INSTALLED
=========

Installed successfully:

* Python 3.13
* Django 6.x
* PostgreSQL 17
* pgAdmin 4
* psycopg2-binary
* Virtual Environment

requirements.txt already created.

==================================================
DATABASE
========

Database Name:

attendance_db

Database connection is already configured successfully.

==================================================
CURRENT PROJECT STATUS
======================

Completed:

✔ Django Project Created

✔ attendance app created

✔ PostgreSQL connected

✔ Initial migrations completed

✔ Superuser created

✔ Django Admin working

==================================================
CURRENT PROJECT STRUCTURE
=========================

Attendance-Management-System/

│
├── attendance/
│   ├── migrations/
│   ├── **init**.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── attendance_system/
│   ├── **init**.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── venv/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore

Create new folders only when they are actually needed.

==================================================
LEARNING STYLE
==============

I am learning Django.

Never dump the whole project.

Always work feature-by-feature.

For every feature follow this workflow:

Design

↓

Code

↓

Migration

↓

Testing

↓

Next Feature

Before writing code:

* Explain the Django concept.
* Explain the database design.
* Explain why we are using a particular approach.
* Explain why it is better than alternatives.
* Follow industry standards.
* Follow clean architecture.
* Follow PEP-8.
* Write scalable code.
* Explain every important line.

I prefer mentoring, not just code dumping.

==================================================
PROJECT MODULES
===============

Current roadmap:

✔ Departments

✔ Employees

⬜ Shifts

⬜ Attendance

⬜ Reports

⬜ Dashboard

⬜ Search

⬜ Filters

⬜ Professional Admin Panel

==================================================
COMPLETED MODEL
===============

Department Model

Completed.

Fields:

* name (unique)

Admin registration completed.

Migration completed.

Admin tested successfully.

==================================================
COMPLETED EMPLOYEE MODEL
========================

Employee model is completed and tested.

Employee IDs are automatically generated in this format:

EMP0001
EMP0002
EMP0003

Employee creation is working correctly from Django Admin.

Employee model already includes:

* Department relationship
* Professional employee ID generation
* Active status
* Created/Updated timestamps
* Proper **str**()
* Admin registration
* Admin customization

Do NOT redesign the Employee model unless absolutely necessary.

==================================================
CURRENT ATTENDANCE MODEL STATUS
===============================

Attendance model has already been designed conceptually.

Fields currently planned:

* employee (ForeignKey)
* attendance_date (DateField with db_index=True)
* status (TextChoices)
* check_in
* check_out
* remarks
* created_at
* updated_at

Meta:

* ordering
* UniqueConstraint(employee, attendance_date)

Relationship:

Department

↓

Employee

↓

Attendance

We have already discussed and understood:

* ForeignKey
* related_name
* TextChoices
* Meta
* ordering
* UniqueConstraint
* db_index
* **str**()
* ValidationError
* clean()
* full_clean()
* save()
* Model-level validation
* Why validation belongs in the model
* Professional project structure

==================================================
VALIDATION DESIGN ALREADY DISCUSSED
===================================

We have already planned:

clean()

↓

_validate_status()

↓

_validate_check_times()

↓

save()

We have also discussed:

* Field-specific ValidationError
* Professional validation
* Separation of responsibilities
* Single Responsibility Principle

==================================================
ATTENDANCE BUSINESS RULES (FINALIZED)
=====================================

Office Start Time:

09:00 AM

Late After:

09:45 AM

Half Day After:

01:30 PM

Office End Time:

06:00 PM

Status Rules:

09:00–09:45

↓

Present

09:46–01:30

↓

Late

After 01:30

↓

Half Day

If no Check-In:

Admin manually selects:

* Absent
* Leave

Reason:

Absent should never be auto-generated because employees may be on approved leave, client visit, biometric failure, etc.

==================================================
IMPORTANT DESIGN DECISION
=========================

We decided to use Option B.

Meaning:

System automatically calculates:

* Present
* Late
* Half Day

Admin manually chooses:

* Absent
* Leave

We also discussed that a Shift model is the better long-term architecture instead of hardcoding office timings.

Recommended Shift fields:

* name
* start_time
* end_time
* late_after
* half_day_after

Employee will be linked with a Shift.

Attendance will calculate status using the assigned Shift.

This is our preferred professional architecture.

==================================================
CODING RULES
============

Never skip explanations.

Never jump multiple steps.

Never redesign completed modules without a valid architectural reason.

Always explain before coding.

Always use industry standards.

Always tell me why one approach is better than another.

Never generate unnecessary migrations.

Review model design before migration.

==================================================
CURRENT STAGE
=============

Continue exactly from here.

Do NOT repeat previous setup.

Do NOT recreate completed models.

Do NOT explain Django basics again.

The next task is:

Design and implement the Shift model professionally so that Attendance status can be calculated dynamically instead of using hardcoded timings.

After Shift is completed:

* Link Employee with Shift.
* Then finalize Attendance model.
* Then migration.
* Then admin.
* Then testing.

Continue exactly from this stage.
