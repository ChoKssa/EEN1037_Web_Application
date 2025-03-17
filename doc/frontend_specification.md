# **Front-end Specification - Factory Machinery Status & Repair Tracking System**

## **Authentication & User management**

- `/login/`
  - **Login page** with client-side validation.
  - Redirects to the **dashboard corresponding to the role** after login.
  - Error display in case of incorrect identifiers.

---

## **Machine Management**

- `/machines/`
  - **Table display** with columns : `Name`, `Status`, `Collections`, `Number of warnings`, `Technicians assigned`.
  - **Sort & Filter** machines by status (`OK`, `Warning`, `Fault`) or by collection.
  - First display of **assigned machines** for Technicians and Repairers.
  - Add/modify machine form (only for Managers).
  - Add **warnings** (Technician) and remove warnings (Technician & Repair).
  - You must be able to click on an element (a machine) to be directed to the machine's specific page.
- `/machines/{id}/`
  - **Machine-specific display** with full details in the form of a product sheet.
  - Machine information can be modified or deleted for Managers.
  - Add a new Warning or delete an existing one.
  - Possibility of **assigning** a Technician or Repairer to the machine for Managers, or deleting an assignment.

---

## **Fault Reporting & Tracking**

- `/faults/`
  - Form enabling a **Technician to report a new fault** with description and images.
  - List of **open fault cases** in table form.
  - You must be able to click on an element (a fault case) to be directed to its specific page.
- `/faults/{id}/`
  - **Machine-specific display** with full breakdown details and history of notes (messages and images).
  - Repairers can click on a button to close the fault.
  - Possibility of adding a note with images after the other notes.

---

## **Dashboard & Data visualization**

- `/dashboard/`
  - Managers should see a dashboard summarizing all current machine statuses, but also the ability to drill down and view summaries for different collections of machinery. They can also view the ranking of machines with the most breakdowns. Information should be presented as dynamic graphs via **Chart.js** or **D3.js**, and they can export a global report as a CSV or PDF file.
  - Technicians and Repairers should see the status of the machines to which they are assigned, but they can click on a "see more" button to redirect to `/machines`.
  - Buttons should redirect to `/machines/` and `faults` for more details.

---

## **General Pages**

- `/about/`
  - Presents an overview of the Factory Machinery Status & Repair Tracking System.  
  - Describes the purpose of the system and how it benefits the factory.  
  - Highlights the team behind the project and their roles.
- `/help/`
  - Provides a user guide explaining how to navigate and use the system.  
  - Includes FAQs on common issues.  
  - Covers API documentation for external integrations.
- `/contact/`
  - Displays contact details for technical support.  
  - Includes a form for users to submit issues or inquiries.
- `/terms/`
  - Details user responsibilities and system usage guidelines.  
  - Explains data privacy and security policies.  
  - Outlines how user data is stored and managed.
