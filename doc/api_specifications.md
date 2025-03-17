# **API Specification - Factory Machinery Status & Repair Tracking System**

## **1️⃣ Authentication & User Management**

### **1.1 User Authentication**

#### **Endpoint: `POST /api/login/`**

- **Description**: Authenticates a user.
- **Request Body (JSON):**

  ```json
  {
    "username": "johndoe",
    "password": "securepassword"
  }
  ```

- **Response (Success - 200 OK):**

  ```json
  {
    "username": "johndoe",
    "role": "Technician"
  }
  ```

- **Response (Failure - 401 Unauthorized):**

  ```json
  {
    "error": "Invalid credentials"
  }
  ```

### **1.2 User Management (Manager only)**

#### **Endpoint: `POST /api/users/`**

- **Description**: Creates a new user account.

- **Request Body (JSON):**

  ```json
  {
    "username": "newuser",
    "password": "securepassword",
    "role": "Technician"
  }
  ```

- **Response (Success - 201 Created):**

  ```json
  {
    "id": 5,
    "username": "newuser",
    "role": "Technician"
  }
  ```

#### **Endpoint: `GET /api/users/`** (Manager only)

- **Description**: Retrieves a list of all users.

- **Response:**

  ```json
  [
    {
      "id": 1,
      "username": "manager1",
      "role": "Manager"
    },
    {
      "id": 2,
      "username": "technician1",
      "role": "Technician"
    }
  ]
  ```

#### **Endpoint: `PUT /api/users/{id}/`** (Manager only)

- **Description**: Updates a user's role.
- **Request Body (JSON):**

  ```json
  {
    "user_id": 2,
    "role": "Repair"
  }
  ```

- **Response (Success - 200 OK):**

  ```json
  {
    "id": 5,
    "username": "updateduser",
    "role": "Repair"
  }
  ```

#### **Endpoint: `DELETE /api/users/{id}/`** (Manager only)

- **Description**: Deletes a user account.
- **Response (Success - 204 No Content):**

  ```json
  {}
  ```

---

## **2️⃣ Machine Management**

#### **Endpoint: `GET /api/machines/`**

- **Description**: Retrieves a list of all machines.
- **Query Parameters:**
  - `status` (optional): Filter by machine status (`OK`, `Warning`, `Fault`).
- **Response (Success - 200 OK):**

  ```json
  [
    {
      "id": 101,
      "name": "Conveyor Belt 1",
      "status": "OK",
      "collections": ["Factory Floor 2"],
      "warnings": [],
      "assigned_users": []
    },
    {
      "id": 102,
      "name": "Drill Press",
      "status": "Fault",
      "collections": ["Workshop 1"],
      "warnings": [],
      "assigned_users": []
    }
  ]
  ```

#### **Endpoint: `POST /api/machines/`** (Manager only)

- **Description**: Adds a new machine.
- **Request Body:**

  ```json
  {
    "name": "Lathe Machine",
    "status": "OK",
    "collections": ["Workshop 3"]
  }
  ```

- **Response (Success - 201 Created):**
  
  ```json
  {
    "id": 1,
    "name": "Lathe Machine",
    "status": "OK",
    "collections": ["Workshop 3"],
    "warnings": [],
    "assigned_users": []
  }
  ```

#### **Endpoint: `PUT /api/machines/{id}/`** (Manager only)

- **Description**: Updates a machine's details.
- **Request Body:**

  ```json
  {
    "machine_id": 100,
    "name": "Conveyor Belt 1",
    "collections": ["Workshop 3"],
  }
  ```

- **Response (Success - 200 OK):**
  
  ```json
  {
    "id": 100,
    "name": "Conveyor Belt 1",
    "collections": ["Workshop 3"],
    "status": "OK",
    "warnings": [],
    "assigned_users": [],
  }
  ```

#### **Endpoint: `POST /api/machines/{id}/warnings/`** (Technician only)

- **Description**: Adds a warning to a machine.
- **Request Body:**

  ```json
  {
    "machine_id": 103,
    "message": "Temperature too high"
  }
  ```

- **Response (Success - 200 OK):**
  
  ```json
  {
    "id": 103,
    "name": "Conveyor Belt 1",
    "status": "Warning",
    "collections": ["Factory Floor 2"],
    "warnings": [
      {
        "id": 1,
        "by": 5,
        "created_at": "2024-03-14T12:00:00Z",
        "message": "Temperature too high"
      }
    ],
    "assigned_users": []
  }
  ```

#### **Endpoint: `DELETE /api/machines/{id}/warnings/{id}`**

- **Description**: Deletes a machine warning.
- **Response (Success - 200 OK):**

  ```json
  {
    "id": 103,
    "name": "Conveyor Belt 1",
    "status": "Warning",
    "collections": ["Factory Floor 2"],
    "warnings": [],
    "assigned_users": []
  }
  ```

#### **Endpoint: `POST /api/machines/{id}/assign-users/`** (Manager only)

- **Description**: Assigns Technicians and Repairers to a machine.
- **Request Body:**

  ```json
  {
    "assigned_users": [3, 4]
  }
  ```

- **Response (Success - 200 OK):**
  
  ```json
  {
    "id": 103,
    "name": "Conveyor Belt 1",
    "status": "Warning",
    "collections": ["Factory Floor 2"],
    "warnings": [
      {
        "id": 1,
        "by": 5,
        "created_at": "2024-03-14T12:00:00Z",
        "message": "Temperature too high"
      }
    ],
    "assigned_users": [
      {
        "id": 3,
        "username": "technician1",
        "role": "Technician"
      },
      {
        "id": 4,
        "username": "repairer1",
        "role": "Repair"
      }
    ]
  }
  ```

#### **Endpoint: `DELETE /api/machines/{id}/assign-users/`** (Manager only)

- **Description**: Removes assigned Technicians and Repairers from a machine.
- **Request Body:**

  ```json
  {
    "assigned_users": [3]
  }
  ```

- **Response (Success - 200 OK):**
  
  ```json
  {
    "id": 103,
    "name": "Conveyor Belt 1",
    "status": "Warning",
    "collections": ["Factory Floor 2"],
    "warnings": [
      {
        "id": 1,
        "by": 5,
        "created_at": "2024-03-14T12:00:00Z",
        "message": "Temperature too high"
      }
    ],
    "assigned_users": [
      {
        "id": 4,
        "username": "repairer1",
        "role": "Repair"
      }
    ]
  }
  ```

#### **Endpoint: `DELETE /api/machines/{id}/`** (Manager only)

- **Description**: Deletes a machine.
- **Response (Success - 204 No Content):**

  ```json
  {}
  ```

---

## **3️⃣ Fault Reporting & Repair Management**

#### **Endpoint: `POST /api/faults/`** (Technician only)

- **Description**: Creates a new fault report.
- **Request Body:**

  ```json
  {
    "machine_id": 102,
    "description": "Motor failure detected"
  }
  ```

- **Response (Success - 201 Created):**
  
  ```json
  {
    "id": 1,
    "machine": 102,
    "reported_by": 2,
    "description": "Motor failure detected",
    "status": "Open",
    "created_at": "2024-03-14T12:00:00Z",
    "images": [],
    "notes": []
  }
  ```

#### **Endpoint: `POST /api/faults/images`** (Technician only)

- **Description**: Upload multiple images for a fault case.
- **Request Body (multipart/form-data)**:

  ```form
    fault_id: 1
    images: [file1.jpg, file2.jpg]
  ```

- **Response (Success - 200 OK):**
  
  ```json
  {
    "id": 1,
    "machine": 102,
    "reported_by": 2,
    "description": "Motor failure detected",
    "status": "Open",
    "created_at": "2024-03-14T12:00:00Z",
    "images": ["http://localhost:8080/img/faults/{fault_id}/file1.jpg", "http://localhost:8080/img/faults/{fault_id}/file2.jpg"],
    "notes": []
  }
  ```

#### **Endpoint: `GET /api/faults/`**

- **Description**: Retrieves all open faults.
- **Response**:
  
  ```json
  [
    {
        "id": 5,
        "machine": 1,
        "reported_by": 2,
        "description": "Motor overheating",
        "status": "Open",
        "created_at": "2024-03-14T12:00:00Z",
        "images": ["http://localhost:8080/img/faults/{fault_id}/file1.jpg", "http://localhost:8080/img/faults/{fault_id}/file2.jpg"],
        "notes": []
    }
  ]
  ```

#### **Endpoint: `POST /api/faults/{id}/`** (Repairer only)

- **Description**: Adds new notes to an fault case and closes it if repair is complete
- **Request Body:**

  ```json
  {
    "notes": "Replaced motor capacitor.",
    "status": "Closed"
  }
  ```

- **Response (Success - 201 Created):**
  
  ```json
  {
        "id": 5,
        "machine": 1,
        "reported_by": 2,
        "description": "Motor overheating",
        "status": "Closed",
        "created_at": "2024-03-14T12:00:00Z",
        "images": ["http://localhost:8080/img/faults/{fault_id}/file1.jpg", "http://localhost:8080/img/faults/{fault_id}/file2.jpg"],
        "notes": [
            {
                "id": 1,
                "by": 5,
                "created_at": "2024-03-16T11:00:00Z",
                "notes": "Replaced motor capacitor.",
                "images": []
            }
        ]
  }
  ```

#### **Endpoint: `POST /api/faults/{id}/images`** (Repairer only)

- **Description**: Upload multiple images for a fault case linked to a note.
- **Request Body (multipart/form-data)**:

  ```form
    note_id: 1
    images: [file1.jpg, file2.jpg]
  ```

- **Response (Success - 200 OK):**
  
  ```json
  {
        "id": 5,
        "machine": 1,
        "reported_by": 2,
        "description": "Motor overheating",
        "status": "Open",
        "created_at": "2024-03-14T12:00:00Z",
        "images": ["http://localhost:8080/img/faults/{fault_id}/file1.jpg", "http://localhost:8080/img/faults/{fault_id}/file2.jpg"],
        "notes": [
            {
                "id": 1,
                "by": 5,
                "created_at": "2024-03-16T11:00:00Z",
                "notes": "Replaced motor capacitor.",
                "images": [["http://localhost:8080/img/faults/{fault_id}/{note_id}/file1.jpg", "http://localhost:8080/img/faults/{fault_id}/{note_id}/file2.jpg"]]
            }
        ]
  }
  ```

---

## **4️⃣ Dashboard & Reports**

#### **Endpoint: `GET /api/dashboard/`** (Manager only)

- **Description**: Retrieves statistics on machine statuses and fault trends.
- **Response (Success - 200 OK):**

  ```json
  {
    "total_machines": 50,
    "ok": 40,
    "warnings": 5,
    "fault": 5
  }
  ```

#### **Endpoint: `GET /api/reports/?format=[csv|pdf]`** (Manager only)

- **Description**: Exports machine data in CSV or PDF format.

- **Response (Success - 200 OK):**

  ```json
  {
    "file": "http://localhost:8080/reports/{report_id}.pdf"
  }
  ```

---

## **5️⃣ Security & Access Control**

- All API requests must be **authenticated via JWT tokens**.
- Managers have full **CRUD access**.
- Technicians can **report faults**.
- Repairers can **update and resolve faults, and add images**.
- View-only users can **only retrieve machine data**.
