# Pokie-Dokie Backend

A Django REST Framework backend with JWT authentication.

## Project Structure

```
pokie/
├── apps/                    # Application modules
│   └── accounts/           # User management app
├── config/                 # Project configuration
├── core/                   # Core functionality
├── media/                  # User-uploaded files
├── static/                 # Static files
├── templates/              # HTML templates
├── .env                    # Environment variables
├── manage.py              # Django management script
└── requirements.txt       # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

The API documentation is available at `/api/docs/` when running the server.

## Features

- JWT Authentication
- User Registration and Management
- RESTful API
- Swagger Documentation
- CORS Support 