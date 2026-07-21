# Attendance Management System

A production-ready Employee Attendance Management System built with Django and PostgreSQL. The system provides secure authentication, employee management, attendance tracking, reporting, and an administrative dashboard suitable for small to medium organizations.

---

## Project Overview

The Attendance Management System helps organizations manage employees and track attendance efficiently through a modern web application.

It includes:

- Secure Authentication
- Employee Management
- Department Management
- Attendance Tracking
- Automatic Attendance Status Calculation
- Attendance Reports
- Dashboard Analytics
- Password Management
- Production Ready Configuration

---

## Features

### Authentication

- Secure Login
- Logout
- Forgot Password
- Password Reset via Email
- Change Password
- Admin Reset Employee Password
- Password Validation
- Force Password Change on First Login

---

### Employee Management

- Employee CRUD
- Automatic Employee ID Generation
- Employee Search
- Employee Filters
- Pagination
- Employee Status Management

---

### Department Management

- Department CRUD
- Department-wise Employee Management

---

### Attendance Management

- Check In
- Check Out
- Manual Attendance Entry
- Attendance History
- Attendance Details
- Working Hours Calculation
- Automatic Attendance Status

Attendance Statuses:

- Present
- Late
- Half Day
- Absent

---

### Reports

- Dashboard Statistics
- Attendance Statistics
- Late Report
- Absent Report
- Department Report
- Working Hours Report
- Interactive Charts using Chart.js

---

### Dashboards

#### Admin Dashboard

- Employee Statistics
- Attendance Statistics
- Recent Attendance
- Reports
- Charts

#### Employee Dashboard

- Personal Attendance
- Monthly Statistics
- Attendance History
- Profile Information

---

### Email System

- Employee Account Email
- Forgot Password Email
- Password Reset Token
- Gmail SMTP Integration

---

### Security

- Environment Variables
- Django Secret Key Protection
- WhiteNoise
- Production Security Settings
- CSRF Protection
- Secure Password Validation

---

## Tech Stack

### Backend

- Python 3.13
- Django

### Database

- PostgreSQL

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js

### Deployment

- Render
- Neon PostgreSQL
- Gunicorn
- WhiteNoise

### Version Control

- Git
- GitHub

---

## Project Structure

```
attendance-management-system/
│
├── attendance/
├── attendance_system/
├── static/
├── templates/
├── media/
├── manage.py
├── requirements.txt
├── runtime.txt
├── build.sh
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/attendance-management-system.git
```

Navigate into the project

```bash
cd attendance-management-system
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file and configure your environment variables.

Run migrations

```bash
python manage.py migrate
```

Run the development server

```bash
python manage.py runserver
```

---

## Environment Variables

Create a `.env` file with the following variables:

```
SECRET_KEY=

DEBUG=

DATABASE_URL=

EMAIL_HOST=

EMAIL_PORT=

EMAIL_HOST_USER=

EMAIL_HOST_PASSWORD=

EMAIL_USE_TLS=

DEFAULT_FROM_EMAIL=
```

---

## Production Deployment

Designed for deployment using:

- Render
- Neon PostgreSQL
- Gunicorn
- WhiteNoise

---

## Future Improvements

- Leave Management
- Holiday Calendar
- Shift Management
- Payroll Integration
- Face Recognition Attendance
- QR Code Attendance
- REST API
- Mobile Application
- Notifications
- Export Reports (PDF/Excel)

---

## License

This project is created for learning, portfolio, and educational purposes.

---

## Author

Gaurav Chaudhary

BCA Student

Python & Django Developer

Aspiring Data Analyst