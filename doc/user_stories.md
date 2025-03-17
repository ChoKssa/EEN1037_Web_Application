# **User Stories - Factory Machinery Status & Repair Tracking System**

## **1️⃣ Authentication & User Management**

### **Manager**

- ✅ *As a Manager, I want to create user accounts with a specific role so that I can manage application access.*
- ✅ *As a manager, I want to delete a user in order to control access to the application.*
- ✅ *As a manager, I'd like to see the list of users and their roles to ensure proper access management.*
- ✅ *As a manager, I'd like to change a user's role so that I can adapt his permissions if necessary.*

### **All Users**

- ✅ *As a user, I want to log in with a username and password.*
- ✅ *As a user, I want my password to be securely stored (hashed and encrypted).*
- ✅ *As a user, I want to log out easily.*
- ✅ *As a user, I want to receive an error message if my credentials are incorrect.*
- ✅ *As a user, I want my role to determine my accessible actions.*

---

## **2️⃣ Machine Management**

### **Manager**

- ✅ *As a Manager, I want to add a machine to maintain an up-to-date list of equipment.*
- ✅ *As a Manager, I want to modify a machine’s information (name, location, status, etc.).*
- ✅ *As a Manager, I want to delete outdated or decommissioned machines.*
- ✅ *As a Manager, I want to assign machines to specific Technicians and Repairers to distribute workload efficiently.*

### **Technician / Repairer**

- ✅ *As a Technician, I want to see the machines assigned to me first on my dashboard.*
- ✅ *As a Technician, I want to view all machines along with their current status (OK, Warning, Fault).*
- ✅ *As a Technician, I want to add a warning (Warning) to a machine if I detect an anomaly.*
- ✅ *As a Repairer, I want to see all machines currently marked as Fault.*

### **View-only User**

- ✅ *As a View-only user, I want to see the list of machines without being able to modify data.*

---

## **3️⃣ Fault Reporting & Repair Management**

### **Technician**

- ✅ *As a Technician, I want to report an issue by creating a Fault Case for a machine.*
- ✅ *As a Technician, I want to add a description and an image to a fault report.*

### **Repairer**

- ✅ *As a Repairer, I want to see all open fault cases that need attention.*
- ✅ *As a Repairer, I want to add notes or images to a fault case to document my intervention.*
- ✅ *As a Repairer, I want to mark a fault case as resolved once the machine is repaired.*

---

## **4️⃣ Dashboard & Data Visualization**

### **Manager**

- ✅ *As a Manager, I want to see a dashboard summarizing machine statuses (OK, Warning, Fault).*
- ✅ *As a Manager, I want to see statistics about the most frequent failures.*
- ✅ *As a Manager, I want to see a ranking of machines with the most failures.*
- ✅ *As a Manager, I want to export these reports in CSV or PDF format.*

### **Technician / Repairer**

- ✅ *As a Technician/Repairer, I want to see a summary of past interventions on assigned machines.*

---

## **5️⃣ External API & Integration**

### **Alert API**

- ✅ *As an external system, I want to send an HTTP request to the API to signal a warning or a fault on a machine.*

### **REST API**

- ✅ *As an integrator, I want a REST API that allows me to retrieve the status of machines in JSON format.*
- ✅ *As an integrator, I want an API that allows me to retrieve the list of open fault cases and their history.*

---

## **6️⃣ Security & Access Control**

- ✅ *As an unauthenticated user, I shouldn't be able to access the application.*
- ✅ *As a user, my access must be limited according to my role (for example, a technician cannot add a new user).*
- ✅ *As an administrator, I want to see failed login attempts for security monitoring.*
