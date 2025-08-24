# Blog Application


This project provides a secure Django REST API with  token-based jwt authentication for tickt.

## 🌟 Features

- token authentication with pyjwt
- Account, Blogs

## 🔧 Technology Stack

- **Backend**: Django 5.2+
- **Database**: PostgreSQL 16+
- **API**: Django REST Framework

## 📋 Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.12+ 
- PostgreSQL 16+
- Git
- pip
- virtualenv (optional for development)

## 🚀 Getting Started

Follow these steps to set up and run the project locally:

### 1. Clone the Repository

```bash
git git@github.com:anish-gc/blog-application.git
cd blog-application
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r development.txt
```

### 4. Configure PostgreSQL

Make sure PostgreSQL is installed and running. Create a database for the project:

```bash
# Access PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE ticket_management_system;

# Exit PostgreSQL
\q
```

### 5. Environment Variables

Create a `.env` file in the project root (You can take sample from .env-sample. Just copy all the contents to .env):

```

SECRET_KEY=django-insecure-s9$(gxq%!vh*v3ex%5)+mzjpl@1&q889tm&s-5=hkgw4snpf#*

# Database Configuration
DB_USER=postgres
DB_PASSWORD=urpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=blog_application

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,api.vynspireailabs.tezhni.com,vynspireailabs.tezhni.com

# Security Settings - Disabled for local development
DEBUG=True
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# CSRF Trusted Origins (for your API and frontend domains)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.vynspireailabs.tezhni.com,https://vynspireailabs.tezhni.com

# CORS Settings (allow your frontend to access the API)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,https://vynspireailabs.tezhni.com

# JWT Configuration
JWT_SECRET_KEY=vynspirelabs
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create a Superuser

```bash
python manage.py createsuperuser
```


### 9. Run the development Server

```bash
python manage.py runserver
The application should now be accessible at http://localhost:8000.
```


```
## 🗂️ Project Structure

```
```
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── management
│   ├── manager.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── authentication
│   ├── urls.py
│   ├── validation.py
│   └── views.py
├── blogs
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── debug.log
├── development.txt
├── manage.py
├── readme.md
├── static
├── utilities
│   ├── decorators.py
│   ├── global_functions.py
│   ├── jwt_utils.py
│   ├── middleware.py
│   ├── mixins.py
│   └── models.py


```

# API Documentation

## Authentication

### User Registration & Login

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register a new user account |
| `/api/auth/login/` | POST | User login authentication |

## Blogs

### Post Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/posts/` | GET | List all posts |
| `/api/posts/my-posts/` | GET | List current user's posts |
| `/api/posts/create/` | POST | Create new post |
| `/api/posts/<int:post_id>/` | GET | Retrieve specific post details |
| `/api/posts/<int:post_id>/update/` | PUT, PATCH | Update specific post |
| `/api/posts/<int:post_id>/delete/` | DELETE | Delete specific post |

### Notes
```
Authentication is required for creating, updating, and deleting posts.
Users can only access their own posts through the my-posts endpoint.
``` 
```

