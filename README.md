# ConfHub - Conference Management System

A web-based, role-based Conference Management System developed as a mini project using Python and Flask. The system provides a centralized platform for managing conferences, paper submissions, reviews, presentations, and attendees.

## ✨ Key Features

- Multi-role authentication for:
  - Admin
  - Organizer
  - Author
  - Reviewer
  - Attendee
- Conference creation and management
- Research paper submission with file upload
- Plagiarism simulation check
- Reviewer assignment and review management
- Paper status workflow:
  - Submitted
  - Accepted
  - Rejected
  - Revised
- Presentation scheduling
- PDF certificate generation
- Attendee registration and conference browsing
- Role-based dashboards and user interfaces
- Organizer dashboard with analytics

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy

### Frontend
- HTML
- CSS
- Bootstrap 5
- Font Awesome

### Database
- SQLite

### Other Technologies
- ReportLab for PDF generation
- Werkzeug for password hashing and session security

## 📁 Project Structure

```text
conference-management-system/
│
├── routes/              # Application routes and role-based modules
├── templates/           # HTML templates and role-specific pages
├── uploads/             # Uploaded files
├── app.py               # Main Flask application
├── config.py            # Application configuration
├── models.py            # Database models
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignored files
