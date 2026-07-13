# 🎓 CampSpark ERP System

CampSpark is an AI-powered College Management ERP System developed using Django, PostgreSQL, Bootstrap, and Python. The platform automates academic and administrative activities and provides a centralized system for students, faculty, and administrators.

---

## 🌐 Live URL & Repository Links
* **Live Deployment**: [https://campspark-production.up.railway.app/](https://campspark-production.up.railway.app/)
* **GitHub Repository**: [https://github.com/Dominicsavio6506/CampSpark](https://github.com/Dominicsavio6506/CampSpark)

---

## 🔑 Seeded Test Credentials (for Reviewers)
Use the following credentials to explore the different roles on the live site:

| Role | Username | Password | Access Details |
|---|---|---|---|
| **Administrator** | `admin` | `adminpass` | Full admin panel access, database views |
| **Faculty Staff** | `staff1` to `staff12` | `staffpass` | Attendance submission, grading, student projects |
| **Student** | `student1` to `student30` | `studpass` | Personal dashboard, results, library, fee receipts |

---

## 🔒 Recent Security & Architectural Updates
We recently completed a comprehensive code audit and reconstruction pass:
- **Certificate Ownership Checks**: Secured PDF certificate generation (Bonafide, Semester Results, Fee Certificates) with ownership guards, allowing students to access only their own files while preserving access for staff and superusers.
- **Reminders Routing**: Wired up `dashboard.urls` under the core project configuration, enabling active reminder badge counts and focus updates.
- **Accurate Fee Calculation**: Restructured model operations to prevent double-counting on fee edits and updated scholarship logic to adjust by difference rather than raw re-applications.
- **Safe Analytics Reporting**: Wrapped data processing functions in Excel reports to handle missing profiles without crashing.

---

# 🚀 Features

- Student Management
- Staff Management
- Attendance Tracking
- Fee Management
- Library Management
- Event Management
- Complaint Management
- AI Assistant Chatbot
- Notifications & Smart Reminders
- Dashboard Analytics
- Student Project Management
- Report Generation
- Role-Based Authentication
- Cloud Deployment Support

---

# 🛠 Technology Stack

## Backend
- Python
- Django

## Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

## Database
- PostgreSQL
- SQLite

## Tools & Services
- GitHub
- Railway
- Chart.js
- Whitenoise

---

# 📂 System Modules

- Authentication & User Roles
- Student Dashboard
- Staff Dashboard
- Admin Panel
- Attendance Module
- Fee Management Module
- Library Module
- Event Management Module
- Complaint & Grievance Module
- Notification System
- Reports & Analytics
- Student Project Management
- AI Assistant Module

---

# 🤖 AI Integration

CampSpark integrates a advanced AI chatbot powered by the **Groq API (Llama-3.3-70B model)**. The integration includes:
- **Intelligent Routing**: Checks user queries for keywords related to attendance, fees, marks, library books, and events.
- **Context Injection**: Dynamically injects live ERP metrics (total students, active events, fee totals, etc.) into the prompt context when a user asks ERP-related questions, ensuring responses are accurate and reflect real-time campus data.
- **Domain Guarding**: Restricts the assistant's scope to campus-related topics only, blocking off-topic conversations.
- **Conversation Logs**: Automatically saves chat history locally in the database for faculty and staff reviews.

---

# 📸 System Screenshots

## Login Page

![Login_Page](screenshots/Login_page.png)

## Student Dashboard

![Student Dashboard](screenshots/Student_dashboard_1.png)

## Staff Dashboard

![Staff Dashboard](screenshots/Staff_dashboard.png)

## Admin Dashboard

![Admin Dashboard](screenshots/Admin_dash_board.png)

## AI Assistant

![AI Assistant](screenshots/Camspark_AI.png)

## Complaint Management

![Complaint Module](screenshots/Complaint_management_page.png)

## Event Management

![Events Module](screenshots/Event_home_page.png)

## Library Module

![Library Module](screenshots/Library_control_page.png)

## Notifications

![Notification Module](screenshots/Notification_page.png)

## Smart Reminder Popup

![Smart Popup](screenshots/Smart_popup.png)

## Project Management

![Projects](screenshots/Project_home_page.png)

---

# ⚙ Installation

Clone repository:

```bash
git clone https://github.com/Dominicsavio6506/CampSpark.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

---

# ☁ Deployment

CampSpark has been deployed using Railway cloud hosting with PostgreSQL database support.

---

# 🔮 Future Enhancements

- Mobile Application
- Advanced AI Analytics
- Multi-College Support
- Biometric Attendance
- Enhanced Security Features
- Android Application
- AI-based Student Performance Prediction

---

# 👨‍💻 Developer

### Dominic savio

**B.Sc Computer Science**

Government Arts and Science College, Manapparai

### Skills

- Python
- Django
- PostgreSQL
- Bootstrap
- HTML
- CSS
- JavaScript
- AI Integration
- REST API

### GitHub

https://github.com/Dominicsavio6506

### LinkedIn

https://www.linkedin.com/in/dominic-savio-66b5792ba

---

## ⭐ If you found this project useful, consider giving it a star.
