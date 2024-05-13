# Hospital Management System

## Overview
This Hospital Management System is designed to streamline the operations of a hospital by providing a centralized platform for managing patients, doctors, nurses, medicines, equipment, appointments, and administrative tasks. The system utilizes Django for the backend and Firebase for realtime data management, ensuring efficient communication and data synchronization across all users and devices.

## Features

- **User Roles**: The system supports multiple user roles including Patient, Doctor, Nurse, Medicine Manager, Equipment Manager, Appointment Manager, and Director of Hospital, each with specific permissions and functionalities tailored to their role.
- **Realtime Data Management**: Firebase integration enables realtime data updates, ensuring that changes made by one user are instantly reflected for all other users accessing the system.
- **Patient Management**: Patients can register, schedule appointments, view medical records, and communicate with healthcare providers.
- **Doctor and Nurse Management**: Healthcare providers can manage their schedules, view patient information, update medical records, and communicate with patients.
- **Inventory Management**: Medicine and Equipment Managers can track inventory levels, manage stock, and place orders as needed.
- **Appointment Management**: Appointment Managers can schedule, reschedule, and cancel appointments, ensuring efficient allocation of resources and minimizing wait times for patients.
- **Director of Hospital Responsibilities**: The Director of Hospital has access to the following additional features:
  - **User Management**: Ability to manage user accounts, including creating new accounts, modifying permissions, and disabling accounts as needed.
  - **Staff Schedule Management**: Ability to create and manage schedules for hospital staff, ensuring adequate coverage for all shifts and departments.
  - **Staff Addition**: Ability to add new staff members to the system, including assigning roles and permissions.

## Installation
To run the Hospital Management System locally, follow these steps:

1. Install Django:
    ```bash
    pip3 install django
    ```
2. Install Firebase Admin SDK:
    ```bash
    pip3 install firebase-admin
    ```
3. Clone this repository:
    ```bash
    git clone https://github.com/your-username/hospital-management-system.git
    ```
4. Navigate to the project directory:
    ```bash
    cd hospital-management-system
    ```
5. Run the Django server:
    ```bash
    python3 manage.py runserver
    ```
6. Access the application at [http://localhost:8000](http://localhost:8000) in your web browser.

## Contact
For any inquiries or support, please contact [binh.nguyendangthanh@hcmut.edu.vn](binh.nguyendangthanh@hcmut.edu.vn).
