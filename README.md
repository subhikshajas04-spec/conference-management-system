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
🚀 Installation and Setup
1. Clone the Repository
git clone https://github.com/subhikshajas04-spec/conference-management-system.git
2. Navigate to the Project Directory
cd conference-management-system
3. Install Required Dependencies
py -m pip install -r requirements.txt
4. Run the Application
py app.py
5. Open the Application

Open your web browser and visit:

http://127.0.0.1:5000

The application will create the required database when it is started.

🔐 User Roles

The system supports different roles with role-specific functionalities:

Role	Main Responsibilities
Admin	Manage users and system operations
Organizer	Create conferences, manage papers, assign reviewers, and schedule presentations
Author	Submit papers and track submission status
Reviewer	Review assigned papers and submit reviews
Attendee	Browse conferences and register for events
📌 Project Purpose

The purpose of ConfHub is to simplify and centralize conference management activities through a single web-based platform. The project demonstrates the implementation of role-based access, database management, file handling, paper review workflows, conference scheduling, and PDF generation using Flask.

🔮 Future Improvements
Email notifications for paper status updates
Integration with real plagiarism detection APIs
Online payment integration for conference registration
Cloud-based file storage
Deployment to a production web server
Advanced analytics and reporting
👩‍💻 Project Type

Mini Project

Developed using: Python, Flask, SQLite, HTML, CSS, Bootstrap, and JavaScript


After you paste it into `README.md`, click **Commit changes** with this message:

```text
Improve project README documentation
