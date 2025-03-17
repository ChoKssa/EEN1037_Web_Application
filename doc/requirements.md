# **Requirements Specification - Factory Machinery Status & Repair Tracking System**

## **1️⃣ Functional Requirements**

### **1.1 Authentication & User Management**

#### **Backend Requirements**

- The system **must support user authentication** using **session-based authentication** (for web application) and **API Keys** (for external use).
- Users must be able to **log in** with their **username and password**.
- Passwords must be **hashed and stored securely**.
- A **Manager** must be able to:
  - **Create, modify, and delete user accounts.**
  - **Assign a role** to each user (**Manager, Technician, Repair, View-only**).
  - **Retrieve the list of all users and their roles.**
- Unauthorized users must be **denied access** to protected resources.
- **Failed login attempts** must be recorded for security monitoring.

#### **Frontend Requirements**

- The login page must provide **form validation** and display **error messages** for invalid credentials.
- The user must be redirected to their respective **dashboard** after login.
- The interface must adjust dynamically **based on user role**.

---

### **1.2 Machine Management**

#### **Backend Requirements**

- The system must support **CRUD operations** for machines.
- Machines must have the following attributes:
  - `name`: Machine name (String, required)
  - `status`: One of **OK, Warning, Fault** (Enum, required)
  - `collections`: multiple user-definable strings matching regex **[A-Za-z0-9\\-]**
  - `assigned_users`: Many-to-Many relationship with Technicians and Repairers.
  - `warnings`: Warning messages added by Technicians and removed by Repairers.
- The **Manager** must be able to:
  - **Add, edit, and delete machines.**
  - **Assign machines to users.**
- **Technicians** and **Repairers** must be able to view the machines they are assigned to first and the other machines.

#### **Frontend Requirements**

- Machines must be displayed in **a table format**, sortable and filterable by status.
- **Technicians** and **Repairers** must see **assigned machines first**.
- **Managers** must have an interface to **add, modify, and delete machines**.

---

### **1.3 Fault Reporting & Repair Management**

#### **Backend Requirements**

- The system must support **Fault Case** creation and management.
- Fault Cases must have:
  - `machine_id`: Associated machine (ForeignKey)
  - `reported_by`: Technician who reported the fault (ForeignKey)
  - `description`: Text field for details.
  - `images`: Optional file upload.
  - `status`: Open / Closed.
  - `notes`: notes added while Repairers are working on the case.
- **Technicians** must be able to **report faults** with a description and images, and update them by adding notes later.
- **Repairers** must be able to **update fault cases**, adding notes/images.
- **Repairers** must be able to **mark a fault case as resolved**.

#### **Frontend Requirements**

- **Technicians** must be able to fill out a form to **report a fault**.
- **Repairers** must have a **dashboard listing open fault cases**.
- A fault case page must allow:
  - Viewing fault details.
  - Adding notes/images.
  - Marking the fault as resolved.

---

### **1.4 Dashboard & Data Visualization**

#### **Backend Requirements**

- The system must generate:
  - **Statistics on fault frequency**.
  - **Summaries of machine status distribution**.
  - **Exportable reports in CSV/PDF format**.

#### **Frontend Requirements**

- **Managers** must have a dashboard with:
  - A **graphical overview** of machine statuses (OK, Warning, Fault).
  - **Historical trends** for faults and repairs.
- Reports must be downloadable in **CSV and PDF format**.

---

### **1.5 External API & Integration**

#### **Backend Requirements**

- The system must expose **REST API endpoints** for:
  - **Machine status retrieval** (`GET /api/machines/`)
  - **Fault case retrieval** (`GET /api/faults/`)
  - **Fault reporting by external systems** (`POST /api/faults/` with JSON payload)
- API requests must require **authentication** (API key).

#### **Frontend Requirements**

- Internal system calls must use AJAX/Fetch API for **dynamic updates**.
- **Admins** must be able to configure API keys for external systems.

---

## **2️⃣ Non-Functional Requirements**

### **2.1 Performance & Scalability**

- The system must handle **at least 100 concurrent users**.
- API response times should be **under 500ms** for most requests.
- Database queries must be **optimized using indexes** where applicable.

### **2.2 Security**

- All sensitive data (passwords) must be **encrypted**.

### **2.3 Deployment & Maintainability**

- The system must run in **Docker containers**.
- **CI/CD pipelines** must automate testing and deployment.
- A **logging system** must track API requests, authentication attempts, and system errors.

---

## **3️⃣ System Constraints**

- **Programming Language**: Python (Django)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (with optional frameworks)
- **Hosting**: Cloud-based (Docker-compatible)
