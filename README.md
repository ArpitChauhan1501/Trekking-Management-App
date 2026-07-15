# TrekMate - Trekking Management System

## Overview

TrekMate is a web-based Trekking Management System developed using Flask. It provides a platform for administrators, staff members, and users to efficiently manage trekking activities. The system allows administrators to manage treks, assign staff, monitor bookings, and manage users, while users can browse and book available treks.

---

## Features

### Authentication
- User Registration
- User Login & Logout
- Secure Password Hashing
- Role-Based Authentication

### Admin
- Dashboard
- Add, Edit and Delete Treks
- Assign Staff to Treks
- Manage Users
- Manage Staff
- Approve Staff Accounts
- Blacklist / Unblacklist Users
- View Bookings

### Staff
- Dashboard
- View Assigned Treks
- View Bookings for Assigned Treks

### User
- Dashboard
- Browse Available Treks
- Book Treks
- View Booking History

### Profile
- View Profile
- Edit Profile

---

## Technology Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Jinja2

### Backend
- Python
- Flask

### Database
- SQLite
- SQLAlchemy

### Authentication
- Flask-Login
- Werkzeug Security

---

## Project Structure

```
TrekkingManagementApp/
│
├── app.py
├── config.py
├── models.py
├── seed.py
├── requirements.txt
│
├── routes/
│   ├── auth.py
│   ├── admin.py
│   ├── staff.py
│   └── user.py
│
├── templates/
├── static/
├── instance/
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/24f3004260/Trekking-Management-App/blob/main/.gitignore
cd Trekking-Management-App
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create the Database

```bash
python app.py
```

### Create the Default Admin Account

```bash
python seed.py
```

### Run the Application

```bash
python app.py
```

The application will be available at:

```
http://localhost:5000
```

---

## Default Admin Credentials

Email

```
admin@gmail.com
```

Password

```
Admin@123
```

---

## Author

**Arpit Chauhan**

B.Tech Computer Science and Engineering
