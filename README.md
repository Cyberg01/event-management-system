# Event Management System

A production-ready RESTful API for managing technical events and conferences, built with Django 6 and Django REST Framework. This project demonstrates scalable API design, JWT authentication, robust permission handling, and comprehensive documentation.

---

## Features
- User registration, authentication (JWT), and role-based access (admin, organizer, attendee, speaker)
- Event creation, update, deletion, and registration management
- Session and track management with conflict validation
- Venue management with capacity and amenities
- Advanced filtering, searching, and pagination
- Standardized API responses and error handling
- Interactive API documentation (Swagger/OpenAPI)
- Dockerized deployment and environment management

---

## Tech Stack
- Python 3.14+
- Django 6.0+
- Django REST Framework
- drf-spectacular (OpenAPI/Swagger docs)
- PostgreSQL (via Docker)
- Docker & docker-compose

---

## Main Libraries Used

### Core Dependencies
- [Poetry](https://python-poetry.org/) - Dependency management & packaging
- [Django](https://www.djangoproject.com/) 6.0+
- [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/) - JWT authentication
- [drf-spectacular](https://drf-spectacular.readthedocs.io/) - OpenAPI/Swagger documentation
- [django-filter](https://django-filter.readthedocs.io/) - Advanced filtering
- [django-cors-headers](https://pypi.org/project/django-cors-headers/) - CORS handling
- [psycopg](https://www.psycopg.org/) - PostgreSQL adapter
- [dj-database-url](https://pypi.org/project/dj-database-url/) - Database URL parsing
- [Pillow](https://python-pillow.org/) - Image processing

---

## Directory Structure
```
event-management-system/
├── manage.py
├── pyproject.toml
├── requirements.txt / poetry.lock
├── docker-compose.yml
├── Dockerfile
├── deploy.sh
├── README.md
├── .env.example
├── eventmanagementsystem/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── apps/
│   ├── auth/ users/ events/ event_sessions/ registrations/ tracks/ venues/ speakers/ common/
├── docs/
└── media/
```

---

## Database Relationship Diagram

### About the Database Schema

The following diagram and table list describe the main entities (tables) in the Event Management System and their roles:

| Table         | Purpose                                                                 | Key Fields / Description                                                                 |
|-------------- |------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| User          | Django built-in user authentication                                     | username, email, password, is_active, is_staff, etc.                                     |
| UserProfile   | Extended user info and role management                                 | user (FK), bio, role (admin/organizer/attendee/speaker), profile_picture, created_at     |
| Event         | Represents an event or conference                                      | title, description, start_date, end_date, capacity, venue (FK), creator (FK), status     |
| Track         | Logical grouping of sessions within an event                           | name, description, event (FK), created_at                                                |
| Session       | Individual sessions/talks within an event                              | title, description, start_time, end_time, speakers (M2M), track (FK), event (FK), room   |
| Venue         | Physical location for events/sessions                                  | name, address, city, capacity, amenities, venue_image, created_at                        |
| Registration  | User registration for an event                                         | user (FK), event (FK), registered_at, status, check_in_at                                |

**Legend:**
- FK = Foreign Key
- M2M = Many-to-Many


## Setup Instructions

### 1. Clone the repository
```bash
git clone <repo-url>
cd event-management-system
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your database credentials and secret keys
```

### 3. Local Development (without Docker)
```bash
# Install dependencies
poetry install

# Run migrations
poetry run python manage.py migrate

# Create superuser
poetry run python manage.py createsuperuser

# Run the development server
poetry run python manage.py runserver
```

### 4. Development/Production with Docker
With Docker, all dependencies and migrations are handled automatically. You only need to run:
```bash
docker-compose up -d
```
This will build the images, install dependencies (via Poetry), apply migrations, and start the server at http://localhost:8080.

To create a superuser inside the running container:
```bash
docker-compose exec web python manage.py createsuperuser
```

---

## Docker Setup

### Build and run with Docker Compose
```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Environment Variables
See `.env.example` for all required variables:
- `DATABASE_URL`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `JWT_SECRET_KEY`
- `CORS_ALLOWED_ORIGINS`
- ...and more

---

## API Documentation
After running the server u can't API Documentation through this endpoint
- **Swagger UI:** [http://localhost:8080/api/schema/swagger-ui/](http://localhost:8080/api/schema/swagger-ui/)
- **ReDoc:** [http://localhost:8080/api/schema/redoc/](http://localhost:8080/api/schema/redoc/)
- **OpenAPI schema:** [http://localhost:8080/api/schema/](http://localhost:8080/api/schema/)

API endpoints, request/response formats, and error codes are fully documented in Swagger UI.

---

---

## Assumptions & Decisions
- All API responses follow a standardized format
- JWT authentication is required for protected endpoints
- Role-based permissions are strictly enforced
- Database schema is optimized for event management use cases
- Docker is used for local deployments

---

## License
This project is for technical assessment and demonstration purposes.

---

## Author
Ananta Alwy

---

For more details, see the API documentation or contact the author.
