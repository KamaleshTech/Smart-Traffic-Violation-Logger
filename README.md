# 🚦 Smart Traffic Violation Logger

A modern Flask-based web application for managing traffic violation records, generating digital challans, and providing public access to violation and payment status through QR-based verification.

---

## 📌 Overview

**Smart Traffic Violation Logger** is a web-based traffic violation management system designed to simplify the process of recording, managing, searching, and verifying traffic violations.

The system provides a dedicated workflow for **traffic officers** to manage violation records and a separate **public verification workflow** that allows citizens to view violation details and payment status.

The application uses **Flask** for the backend, **SQLite** for lightweight data persistence, **SQLAlchemy** for database operations, and **QR Code technology** for digital challan verification.

---

## ✨ Key Features

### 👮 Officer Management

- Secure officer login and logout
- Session-based authentication
- Add new traffic violation records
- Edit existing violation records
- Delete violation records
- Update violation payment status
- View complete violation history

### 🔎 Search & Filtering

- Search violations using vehicle number
- Filter records by date
- Filter by payment status
- Filter by violation type
- View organized violation records in a responsive table

### 🧾 Digital Challan

- Generate a digital challan for each violation
- Display complete violation information
- Show fine amount and payment status
- Generate a unique QR code
- Print-friendly challan layout

### 📱 QR-Based Public Verification

The QR code on the digital challan provides a simple verification flow:

```text
Digital Challan
      ↓
   QR Code
      ↓
Public Verification
      ↓
Violation Details
      ↓
Payment Status
```

Citizens can scan the QR code and access the public verification page without logging into the officer panel.

### 💳 Demo Payment Flow

- Public users can review unpaid challans
- Payment confirmation flow is available
- Violation status changes from `Unpaid` to `Paid`
- The current implementation is a **demo payment flow**
- No real financial transaction is processed

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy / SQLAlchemy |
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Icons | Bootstrap Icons |
| Template Engine | Jinja2 |
| Authentication | Flask Session + Werkzeug Password Hashing |
| QR Generation | Python `qrcode` |
| Web Server | Flask Development Server |

---

## 🏗️ System Architecture

The application follows a simple layered web architecture.

```text
┌─────────────────────────────────────────────┐
│                PRESENTATION                 │
│                                             │
│        HTML + CSS + Bootstrap + Jinja2      │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│              APPLICATION LAYER              │
│                                             │
│              Flask Backend                  │
│                                             │
│ Authentication                             │
│ CRUD Operations                             │
│ Search & Filtering                          │
│ QR Generation                               │
│ Public Verification                         │
│ Payment Confirmation                        │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                 DATA LAYER                  │
│                                             │
│             SQLite Database                 │
│              SQLAlchemy ORM                 │
└─────────────────────────────────────────────┘
```

---

## 🔄 Application Workflow

### Officer Workflow

```text
Officer
   ↓
Officer Login
   ↓
Dashboard
   ↓
Add / View Violations
   ↓
Edit / Delete / Update Status
   ↓
Generate Digital Challan
   ↓
Display QR Code
```

### Public Workflow

```text
Citizen
   ↓
Check Violation / Scan QR
   ↓
Public Verification Page
   ↓
View Violation Details
   ↓
View Payment Status
   ↓
Demo Payment Confirmation
```

---

## 🗃️ Database Design

The application uses SQLite for lightweight local data persistence.

### User

| Field | Description |
|---|---|
| `id` | Unique user identifier |
| `username` | Officer username |
| `password_hash` | Hashed officer password |

### Violation

| Field | Description |
|---|---|
| `id` | Unique violation identifier |
| `vehicle_number` | Vehicle registration number |
| `violation_type` | Type of traffic violation |
| `location` | Violation location |
| `violation_date` | Date of violation |
| `fine_amount` | Fine amount |
| `status` | Payment status (`Paid` / `Unpaid`) |

---

## 📂 Project Structure

```text
Smart-Traffic-Violation-Logger/
│
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── instance/
│   └── traffic_violations.db
│
├── static/
│   └── css/
│       ├── style.css
│       └── home.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── add_violation.html
│   ├── edit_violation.html
│   ├── history.html
│   ├── challan.html
│   ├── public_status.html
│   ├── vehicle_search.html
│   └── payment.html
│
└── tests/
    └── test_app.py
```

> Runtime files such as the local SQLite database, Python cache files, and generated QR images are excluded from version control through `.gitignore`.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/KamaleshTech/Smart-Traffic-Violation-Logger.git
```

### 2. Navigate to the project

```bash
cd Smart-Traffic-Violation-Logger
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000/
```

---

## 🔐 Authentication

Management operations are protected by officer authentication.

Protected operations include:

- Add Violation
- Violation History
- Edit Violation
- Delete Violation
- Update Payment Status
- Digital Challan

Public operations such as violation verification and public status viewing do not require officer login.

For production deployment, credentials and secret configuration should be moved to secure environment variables.

---

## 🧪 Testing

Basic application flow tests are included in the `tests/` directory.

Run:

```bash
python -m unittest discover -s tests
```

The tests verify important application entry points such as:

- Home page
- Public vehicle search
- Officer login page
- Officer dashboard access

---

## 🖨️ Digital Challan & QR Verification

Each digital challan contains the violation information and a dynamically generated QR code.

The QR code points to the public verification endpoint for the corresponding violation.

```text
Violation Record
       │
       ▼
Digital Challan
       │
       ▼
 QR Code Generated
       │
       ▼
Public Status URL
       │
       ▼
Citizen Verification
```

This provides a simple way to connect the physical/digital challan with a public verification page.

---

## 🎯 Project Objectives

The project focuses on:

- Digitizing traffic violation records
- Reducing manual record handling
- Providing faster violation search
- Simplifying status management
- Generating digital challans
- Enabling QR-based public verification
- Separating officer and public workflows
- Providing a responsive web interface

---

## 🔮 Future Enhancements

Possible future improvements include:

- Role-based access control for multiple officer levels
- Secure environment-based credential management
- PostgreSQL or MySQL for larger deployments
- Real payment gateway integration
- SMS / Email notification support
- Advanced reporting and analytics
- Officer activity logging
- Cloud deployment
- REST API integration
- Automated challan PDF generation
- Vehicle-owner notification system

---

## 📌 Project Status

**Current Status:** Functional Internship Mini Project

Implemented modules include:

- Officer Authentication
- Violation CRUD
- Search & Filtering
- Payment Status Management
- Digital Challan
- QR Code Verification
- Public Status Page
- Demo Payment Confirmation
- Responsive Web Interface

---

## 👨‍💻 Author

**S. Kamalesh**

Computer Science and Engineering

GitHub:  
https://github.com/KamaleshTech

Portfolio:  
https://my-portfolio-kamalesh4.vercel.app/

---

## 📄 Project Purpose

This project was developed as an **internship mini project** to demonstrate practical implementation of:

- Python & Flask web development
- CRUD application design
- Database integration
- Authentication
- QR code generation
- Responsive frontend development
- Public verification workflows

---

## ⭐ Repository

If you find this project useful, consider giving the repository a ⭐.

**Repository:**  
https://github.com/KamaleshTech/Smart-Traffic-Violation-Logger
