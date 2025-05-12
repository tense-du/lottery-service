# Lottery Service

A FastAPI-based service that manages a lottery system where participants can submit ballots and winners are selected automatically. The service includes secure handling of sensitive data and automated winner selection.

## Overview

- Participants can submit ballots for upcoming lotteries (future dates)
- Winner is selected automatically daily at midnight via Celery
- Users can check the winning ballot for any specific date
- Users can lookup winning ballots by participant (id or email)
- Sensitive data (like emails) is encrypted and searchable
- Users can lookup upcoming lotteries with their ballot counts

## Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Database**: PostgreSQL 16
- **Task Queue**: Celery with Redis
- **Containerization**: Docker & Docker Compose
- **Database Migrations**: Alembic

## Architecture

The service follows a clean architecture pattern:

Directory Structure:
```
.
├── app/            # Main application package
│   ├── api/        # API routes and endpoints
│   ├── core/       # Core configuration and security
│   ├── crud/       # Database operations
│   ├── database/   # Database configuration
│   ├── exceptions/ # Custom exception handlers
│   ├── logs/       # Application logs
│   ├── models/     # SQLAlchemy models
│   ├── schemas/    # Pydantic models
│   ├── services/   # Business logic
│   ├── tasks/      # Celery tasks
│   ├── utils/      # Utility functions
│   └── main.py     # Application entry point
├── migrations/     # Alembic database migrations
└── README.md      # Project documentation
```

## Environment Setup

### Prerequisites

- Docker and Docker Compose (for containerized setup)
- Python 3.13 (for local setup)
- PostgreSQL 16 (for local setup)
- Redis (for local setup)

### Environment Variables

The service uses different environment configurations for Docker and local development. The main difference is in the `DATABASE_URL` host:

For Docker (.env.docker):
```env
# Database (Docker)
POSTGRES_USER=postgres_username
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=lottery_db
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}  # Note: host is 'db' (Docker service name)

# Redis (Optional)
REDIS_PASSWORD=your_redis_password

# Application
LOTTERY_DRAW_DATE_MAX_DAYS_AHEAD=30

# Security (Required)
ENCRYPTION_KEY=your_32_byte_key  # Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
HASH_SALT=your_hash_salt        # Generate with: python -c "import secrets; print(secrets.token_hex(16))"

# Celery
CELERY_DEFAULT_QUEUE=lottery_tasks
```

For Local Development (.env):
```env
# Database (Local)
POSTGRES_USER=postgres_username
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=lottery_db
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}  # Note: host is 'localhost'

# Redis (Optional)
REDIS_PASSWORD=your_redis_password

# Application
LOTTERY_DRAW_DATE_MAX_DAYS_AHEAD=30

# Security (Required)
ENCRYPTION_KEY=your_32_byte_key  # Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
HASH_SALT=your_hash_salt        # Generate with: python -c "import secrets; print(secrets.token_hex(16))"

# Celery
CELERY_DEFAULT_QUEUE=lottery_tasks
```

Note: The environment mode (Docker vs Local) is automatically handled:
- In Docker: Set by docker-compose.yml
- In Local: Defaults to "local" mode

### Using Docker (Recommended)

1. Clone the repository and set up environment:
```bash
# Copy environment files
cp .env.example .env.docker

# Edit .env.docker with your settings
# Make sure DATABASE_URL uses 'db' as the host
nano .env.docker
```

2. Start the services:
```bash
docker-compose up --build
```

This will start:
- FastAPI application (http://localhost:8000)
- PostgreSQL database (accessible at 'db:5432' from within Docker network, and at localhost:5432 from your host machine)
- Redis (accessible at 'redis:6379' from within Docker network, and at localhost:6379 from your host machine)
- Celery worker and scheduler
- Database migrations

### Running Locally

First, ensure you have all dependencies installed:
```bash
pipenv install
```

Then, in separate terminals:

```bash
# Terminal 1: FastAPI server
pipenv run uvicorn app.main:app --reload

# Terminal 2: Celery worker
pipenv run celery -A app.tasks.celery_worker worker -Q ${CELERY_DEFAULT_QUEUE} --loglevel=info

# Terminal 3: Celery beat
pipenv run celery -A app.tasks.celery_worker beat --loglevel=info
```

## API Documentation

Once the service is running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 