# Django Library Management System

A beginner-friendly library management system for mini project submission.

## Project Structure
```
library_system/
├── library_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── library/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── library/
│           ├── base.html
│           ├── login.html
│           ├── book_list.html
│           ├── issued_books.html
│           ├── student_dashboard.html
│           └── search_results.html
├── manage.py
└── db.sqlite3
```

## Setup Instructions

### 1. Create Project Directory
```bash
mkdir library_system
cd library_system
```

### 2. Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Django
```bash
pip install django
```

### 4. Create Django Project
```bash
django-admin startproject library_system .
```

### 5. Create Library App
```bash
python manage.py startapp library
```

### 6. Copy the Code Files
Copy all the provided code files into their respective locations.

### 7. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser (Librarian)
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 9. Run the Server
```bash
python manage.py runserver 0.0.0.0:8000
```

### 10. Access the Application
- **Student Login**: http://localhost:8000/
- **Admin Panel (Librarian)**: http://localhost:8000/admin/

## User Roles

### Librarian (Superuser)
- Login via Django Admin Panel (/admin/)
- Add, update, delete books
- Issue books to students
- Mark books as returned
- View all issued books

### Student (Normal User)
- Login via student login page (/)
- View available books
- Search books by title or author
- View their issued books
- See rental duration

## Features
- ✅ Book management (CRUD operations)
- ✅ Issue/Return books
- ✅ Quantity tracking
- ✅ Search functionality
- ✅ Rental days calculation
- ✅ Simple, clean UI

## Default Test Data
After setup, login to admin panel and:
1. Add some books with quantities
2. Create student users (uncheck 'superuser' and 'staff' status)
3. Issue books to students

## Viva Questions Preparation
- Explain MVC vs MVT architecture
- What is ORM in Django?
- Explain ForeignKey relationship
- What are Django migrations?
- Difference between function-based and class-based views
