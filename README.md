# 🚦 Smart Traffic Violation Logger

<div align="center">

### Digital Traffic Violation Management System

A web-based Flask application for recording, managing, searching, and verifying traffic violation records with digital challans and QR-based public verification.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=sqlalchemy)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-orange?logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-Styling-blue?logo=css3)
![QR Code](https://img.shields.io/badge/QR%20Code-Verification-green)

</div>

---

## 📌 About

**Smart Traffic Violation Logger** is a Flask-based web application designed to digitize the management of traffic violation records.

The system provides a dedicated workflow for traffic officers to:

- Record new traffic violations
- Manage existing violation records
- Search and filter violation history
- Update payment status
- Generate digital challans
- Generate QR codes for public verification

Citizens can use the public verification page to view violation details and the current payment status of a challan.

---

## ✨ Features

### 👮 Officer Management

- Officer login and logout
- Session-based authentication
- Add new violation records
- Edit violation records
- Delete violation records
- Update payment status
- View complete violation history

### 🔎 Search & Filter

The system supports:

- Vehicle number search
- Date filtering
- Payment status filtering
- Violation type filtering

### 🧾 Digital Challan

Each violation can be converted into a digital challan containing:

- Challan number
- Vehicle number
- Violation type
- Location
- Violation date
- Fine amount
- Payment status
- QR verification code

### 📱 QR-Based Verification

The QR code provides a simple verification workflow:

```text
Digital Challan
       ↓
    QR Code
       ↓
Public Verification Page
       ↓
Violation Details
       ↓
Payment Status
```

The public verification page does not require officer login.

### 💳 Demo Payment Flow

The application includes a demonstration payment confirmation flow.

```text
Unpaid
   ↓
Review Challan
   ↓
Confirm Payment
   ↓
Paid
```

> This is a demo payment workflow. No real financial transaction is processed.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application backend |
| Flask-SQLAlchemy | Database ORM |
| SQLite | Data persistence |
| Bootstrap 5 | Responsive UI |
| HTML5 | Frontend structure |
| CSS3 | Custom styling |
| Jinja2 | Server-side templating |
| Bootstrap Icons | UI icons |
| QRCode | QR code generation |
| Werkzeug | Password hashing and security |

---

## 🏗️ System Architecture

```text
                    SMART TRAFFIC
                 VIOLATION LOGGER
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
     OFFICER FLOW                PUBLIC FLOW
          │                           │
          ▼                           ▼
     Officer Login             Check Violation
          │                           │
          ▼                           ▼
       Dashboard                 Search Vehicle
          │                           │
    ┌─────┼─────┐                     ▼
    │     │     │               Public Status
    ▼     ▼     ▼                     │
   Add  History  Manage               ▼
            │                    Payment Status
            ▼
      Digital Challan
            │
            ▼
         QR Code
            │
            └──────────────► Public Status
```

---

## 🔄 Application Workflow

### Officer Workflow

```text
Login
  ↓
Dashboard
  ↓
Add Violation
  ↓
Violation History
  ↓
Edit / Delete / Update Status
  ↓
Digital Challan
  ↓
QR Code
```

### Public Workflow

```text
Check Violation
      ↓
Vehicle Number
      ↓
Violation Results
      ↓
Public Status
      ↓
Fine & Payment Status
```

### QR Workflow

```text
Officer Generates Challan
          ↓
      QR Generated
          ↓
    Citizen Scans QR
          ↓
   Public Status Page
          ↓
Violation + Payment Status
```

---

## 🗃️ Database Design

The application uses a lightweight **SQLite database** with SQLAlchemy ORM.

### User Table

| Column | Description |
|---|---|
| `id` | Unique user ID |
| `username` | Officer username |
| `password_hash` | Hashed password |

### Violation Table

| Column | Description |
|---|---|
| `id` | Unique violation ID |
| `vehicle_number` | Vehicle registration number |
| `violation_type` | Type of traffic violation |
| `location` | Location where violation occurred |
| `violation_date` | Date of violation |
| `fine_amount` | Fine amount |
| `status` | Paid / Unpaid |

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
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── home.css
│   └── qrcodes/
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

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/KamaleshTech/Smart-Traffic-Violation-Logger.git
```

### 2. Open the Project

```bash
cd Smart-Traffic-Violation-Logger
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

---

## 🧪 Testing

Basic application tests are available inside the `tests/` directory.

Run:

```bash
python -m unittest discover -s tests
```

The test suite covers important application pages and officer/public access flows.

---

## 🖥️ Application Modules

| Module | Description |
|---|---|
| Home | Landing page and system navigation |
| Officer Login | Authenticated officer access |
| Add Violation | Create a new violation record |
| Violation History | Search, filter and manage records |
| Edit Violation | Modify existing violation details |
| Digital Challan | Generate and view challan |
| Public Status | Public violation verification |
| Vehicle Search | Search violations using vehicle number |
| Payment | Demo payment confirmation |

---

## 🔐 Security

The application uses:

- Session-based officer authentication
- Password hashing using Werkzeug
- Protected management routes
- Public/private workflow separation

For production deployment, sensitive credentials and secret keys should be stored using environment variables or a secure configuration service.

---

## 🎯 Project Objectives

The main objectives of the project are:

- Digitize traffic violation record management
- Reduce dependency on manual records
- Simplify violation searching and filtering
- Provide digital challans
- Enable QR-based public verification
- Provide clear payment status information
- Separate officer management from public verification

---

## 🔮 Future Enhancements

Possible future improvements include:

- Real online payment gateway integration
- SMS and email notifications
- Advanced traffic analytics dashboard
- Role-based access control
- PostgreSQL/MySQL support
- Cloud deployment
- Automated challan PDF generation
- Officer activity logs
- REST API integration
- Vehicle-owner notification system

---

## 📸 Screenshots

### 🏠 Home Page

_Add your Home page screenshot here._

### 👮 Officer Login

_Add your Login page screenshot here._

### ➕ Add Violation

_Add your Add Violation screenshot here._

### 📋 Violation History

_Add your History screenshot here._

### 🧾 Digital Challan

_Add your Digital Challan screenshot here._

### 📱 Public Verification

_Add your Public Status screenshot here._

---

## 📊 Project Highlights

```text
✓ Flask-based web application
✓ SQLite database integration
✓ SQLAlchemy ORM
✓ Officer authentication
✓ Traffic violation CRUD operations
✓ Search & filtering
✓ Digital challan generation
✓ QR-based public verification
✓ Payment status management
✓ Responsive interface
```

---

## 👨‍💻 Author

<div align="center">

### S. Kamalesh

**B.E. Computer Science and Engineering**

[![GitHub](https://img.shields.io/badge/GitHub-KamaleshTech-black?logo=github)](https://github.com/KamaleshTech)

[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20Website-orange)](https://my-portfolio-kamalesh4.vercel.app/)

</div>

---

## ⭐ Repository

If you found this project useful, consider giving it a ⭐ on GitHub.

**GitHub Repository:**

https://github.com/KamaleshTech/Smart-Traffic-Violation-Logger

---

<div align="center">

### 🚦 Smart Traffic Violation Logger

**Digital • Secure • Simple • Verifiable**

</div>
