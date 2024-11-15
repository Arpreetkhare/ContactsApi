# ContactAPI

## Overview
**ContactAPI** is a Django REST Framework (DRF) application for managing and sharing contacts. This API allows users to manage their contacts, send messages, and securely share contact information with authenticated users. The application integrates JWT-based authentication and uses MySQL as the database, providing a secure and scalable solution.

## Features
- **User Authentication:** Register users with JWT-based authentication. Use the token for secure operations.
- **Contact Management:** CRUD operations to add, update, retrieve, and delete contacts.
- **Sharing Contacts:** Share specific contacts with other authenticated users.
- **Messaging:** Send and receive messages between users.
- **Role-Based Access Control:** Admin users can manage contacts, while regular users can only view and modify their own contacts.
- **Secure Authentication:** JWT tokens for secure login and role validation.

## Tech Stack
- **Backend:** Python, Django, Django REST Framework (DRF)
- **Database:** MySQL
- **Authentication:** JWT
- **Deployment:** Docker

## API Endpoints

### **User Authentication**
| **Method** | **Endpoint**      | **Description**                 |
|------------|-------------------|---------------------------------|
| POST       | `/api/auth/register/` | Register a new user             |
| POST       | `/api/auth/login/`    | Login and get JWT token         |
| GET        | `/api/auth/users/`    | List all users                  |

### **Contact Management**
| **Method** | **Endpoint**           | **Description**                |
|------------|------------------------|--------------------------------|
| POST       | `/api/contacts/`           | Create a new contact           |
| GET        | `/api/contacts/`           | List all contacts              |
| GET        | `/api/contacts/<id>/`      | Retrieve a specific contact    |
| PUT        | `/api/contacts/<id>/`      | Update a contact               |
| DELETE     | `/api/contacts/<id>/`      | Delete a contact               |
| POST       | `/api/contacts/<id>/share/` | Share a contact              |
| POST       | `/api/contacts/bulk-delete/` | Bulk delete contacts         |

### **Favorites**
| **Method** | **Endpoint**               | **Description**                |
|------------|----------------------------|--------------------------------|
| GET        | `/api/favorites/`          | Get a list of favorite contacts|
| POST       | `/api/contacts/<contact_id>/toggle-favorite/` | Toggle favorite status of a contact |

### **Messaging**
| **Method** | **Endpoint**               | **Description**                |
|------------|----------------------------|--------------------------------|
| POST       | `/api/msg/send-msg/`       | Send a new message             |
| GET        | `/api/msg/received-msg/`   | Get received messages          |

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/contactapi.git
   cd contactapi
2. **Set up a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Run the application:**
   ```bash
   python manage.py runserver

5. **Build the Docker image:**   
   ```bash
   docker build -t contactapi

6. **Run the Docker container:**
   ```bash
   docker run -d -p 8000:8000 --name contactapi contactapi
   

