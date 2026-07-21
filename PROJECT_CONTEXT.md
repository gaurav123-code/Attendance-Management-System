# PROJECT CONTEXT

## Project Name

Attendance Management System

---

## Objective

Build a production-ready Employee Attendance Management System following Django best practices with clean architecture, PostgreSQL, Bootstrap, and secure authentication.

The project is intended to be portfolio quality and deployable on Render using Neon PostgreSQL.

---

# Technology Stack

Backend

- Python 3.13
- Django

Database

- PostgreSQL

Frontend

- HTML
- CSS
- Bootstrap 5
- JavaScript
- Chart.js

Deployment

- Render
- Neon PostgreSQL
- Gunicorn
- WhiteNoise

Configuration

- python-decouple
- dj-database-url

---

# Core Modules

Authentication

Employee

Department

Attendance

Reports

Dashboard

Email

Deployment

---

# Completed Features

## Authentication

- Login
- Logout
- Forgot Password
- Password Reset
- Change Password
- Admin Reset Password
- Password Validation
- Must Change Password

---

## Employee

- CRUD
- Auto Employee ID
- Search
- Filters
- Pagination

---

## Department

- CRUD

---

## Attendance

- Check In
- Check Out
- Manual Attendance
- Attendance History
- Attendance Details
- Working Hours Calculation
- Automatic Attendance Status
- Automatic Absent Marking

---

## Reports

- Dashboard Statistics
- Attendance Statistics
- Late Report
- Absent Report
- Department Report
- Working Hours Report
- Charts

---

## Dashboard

Admin Dashboard

Employee Dashboard

---

## Email

Forgot Password

Password Reset

SMTP

Employee Credentials

---

## Database

PostgreSQL

---

## Security

Environment Variables

WhiteNoise

Production Settings

CSRF Protection

Secure Password Validation

---

# Attendance Rules

Office Start

09:00 AM

Late

After 09:45 AM

Half Day

After 01:30 PM

Absent

If employee does not check in.

Automatic absent marking is handled using a custom Django Management Command.

---

# Deployment Status

GitHub

Completed

Production Configuration

Completed

Requirements

Completed

Runtime

Completed

Build Script

Completed

Next Steps

- Create Neon PostgreSQL Database
- Configure Render
- Add Environment Variables
- Deploy
- Production Testing

---

# Coding Standards

- PEP-8
- Clean Architecture
- Readable Code
- Minimal Comments
- Reusable Components
- No Hardcoded Secrets

---

# Project Goal

Develop a production-ready attendance management system suitable for portfolio presentation and real-world deployment while following Django best practices.