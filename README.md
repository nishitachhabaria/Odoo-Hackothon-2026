# 🚀 AssetFlow – Enterprise Asset & Resource Management System

> **Built for Odoo Hackathon 2026**
>
> A modern, scalable ERP platform for managing enterprise assets, shared resources, maintenance, audits, and analytics.

---

## 📌 Overview

AssetFlow is an Enterprise Asset & Resource Management System designed to help organizations efficiently manage their physical assets and shared resources.

The platform provides:

- 📦 Asset Lifecycle Management
- 👥 Employee & Department Management
- 🔄 Asset Allocation & Transfer
- 📅 Resource Booking
- 🔧 Maintenance Workflow
- 📋 Asset Audit
- 📊 Reports & Analytics
- 🔔 Notifications
- 📝 Activity Logs
- 🔐 Secure Role-Based Access Control

---

# ✨ Features

## 🔐 Authentication

- JWT Authentication
- Secure Login
- Employee Signup
- Forgot Password
- Role-Based Access Control (RBAC)

Roles:

- 👑 Admin
- 📦 Asset Manager
- 🏢 Department Head
- 👤 Employee

---

## 🏢 Organization Management

- Departments
- Department Hierarchy
- Employee Directory
- Asset Categories
- Role Assignment

---

## 💻 Asset Management

- Register Assets
- QR Code Support
- Asset Images & Documents
- Asset Search
- Asset History
- Asset Tracking

Asset Status

- ✅ Available
- 👤 Allocated
- 📅 Reserved
- 🔧 Under Maintenance
- ❌ Lost
- 🗑 Disposed
- 🏁 Retired

---

## 🔄 Asset Allocation

- Allocate Asset
- Return Asset
- Transfer Requests
- Approval Workflow
- Overdue Tracking

---

## 📅 Resource Booking

Bookable Resources

- Meeting Rooms
- Conference Rooms
- Vehicles
- Projectors
- Shared Equipment

Features

- Calendar View
- Conflict Detection
- Booking History
- Time Slot Validation

---

## 🔧 Maintenance

Workflow

```
Pending
    ↓
Approved
    ↓
Technician Assigned
    ↓
In Progress
    ↓
Resolved
```

Features

- Raise Request
- Approval Workflow
- Technician Assignment
- Maintenance History

---

## 📋 Asset Audit

- Audit Cycles
- Auditor Assignment
- Asset Verification
- Missing Asset Detection
- Discrepancy Reports

---

## 📊 Dashboard

Real-time KPI Dashboard

- Total Assets
- Available Assets
- Allocated Assets
- Active Bookings
- Maintenance Requests
- Departments
- Employees
- Recent Activity
- Notifications

---

## 📈 Reports & Analytics

- Asset Utilization
- Department Reports
- Booking Heatmap
- Maintenance Trends
- Export CSV
- Export PDF

---

## 🔔 Notifications

- Asset Assigned
- Booking Reminder
- Maintenance Updates
- Transfer Approval
- Audit Alerts

---

## 📝 Activity Logs

Track every important action

- Login
- Asset Created
- Asset Updated
- Allocation
- Booking
- Maintenance
- Audit
- Reports

---

# 🖥 Tech Stack

## 🎨 Frontend

- React 19
- TypeScript
- Vite
- Tailwind CSS
- React Router
- TanStack Query
- Axios
- React Hook Form
- Zod
- Recharts
- FullCalendar
- Framer Motion
- Lucide React
- Sonner

---

## ⚙ Backend

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- JWT Authentication
- Pydantic v2

---

## 🗄 Database

- PostgreSQL

---

## ☁ Deployment

Frontend

- Vercel

Backend

- Render

Database

- PostgreSQL

---

# 📁 Project Structure

```text
AssetFlow
│
├── frontend
│   ├── public
│   ├── src
│   │   ├── app
│   │   ├── assets
│   │   ├── components
│   │   ├── constants
│   │   ├── hooks
│   │   ├── layouts
│   │   ├── pages
│   │   │   ├── auth
│   │   │   ├── dashboard
│   │   │   ├── organization
│   │   │   ├── assets
│   │   │   ├── allocations
│   │   │   ├── bookings
│   │   │   ├── maintenance
│   │   │   ├── audits
│   │   │   ├── reports
│   │   │   ├── notifications
│   │   │   └── settings
│   │   ├── routes
│   │   ├── services
│   │   ├── store
│   │   ├── types
│   │   └── utils
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── database
│   │   ├── dependencies
│   │   ├── middleware
│   │   ├── models
│   │   ├── repositories
│   │   ├── schemas
│   │   ├── services
│   │   ├── websocket
│   │   └── main.py
│   │
│   ├── alembic
│   ├── requirements.txt
│   └── .env.example
│
├── docs
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# ⚙ Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```bash
cp .env.example .env
```

Run migrations

```bash
alembic upgrade head
```

Start FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://localhost:8000/docs
```

---

# 🎨 Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 🔑 Default Credentials

```
Email

admin@assetflow.com

Password

Admin@123
```

---

# 🚀 Development Roadmap

- ✅ Project Setup
- ✅ Backend Foundation
- ✅ Authentication
- ✅ Organization Setup
- ✅ Dashboard
- ✅ Asset Management
- ✅ Asset Allocation
- ✅ Resource Booking
- ⏳ Maintenance
- ⏳ Audit
- ⏳ Reports
- ⏳ Notifications
- ⏳ Activity Logs
- ⏳ AI Assistant
- ⏳ Mobile Responsive
- ⏳ Docker Deployment

---

# 🔮 Future Enhancements

- 🤖 AI Asset Assistant
- 📱 Progressive Web App (PWA)
- 📷 QR Scanner
- 📦 Barcode Support
- 📩 Email Notifications
- 💬 WhatsApp Notifications
- 📄 OCR Invoice Scanner
- 📈 Predictive Maintenance
- 🌍 Multi-Organization Support
- ☁ Cloud Storage

---

# 👨‍💻 Team

**AssetFlow Team**

Built with ❤️ for **Odoo Hackathon 2026**

---

# 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

### ⭐ Star this repository if you like the project!

**Happy Coding 🚀**

</div>
