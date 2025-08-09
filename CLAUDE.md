# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Docker-based Development
This project runs in Docker containers. Use these commands for development:

```bash
# Start all services
docker compose up --build -d

# View logs
docker compose logs -f web
docker compose logs -f db

# Run Django commands
docker compose exec web python manage.py migrate
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py test
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput

# Access Django shell
docker compose exec web python manage.py shell

# Access container bash
docker compose exec web bash
```

### Database Management
```bash
# Database migrations
docker compose exec web python manage.py migrate

# Create migrations
docker compose exec web python manage.py makemigrations

# Database backup
docker compose exec db mysqldump -u root -p resume_db > backup.sql

# Database restore
docker compose exec -T db mysql -u root -p resume_db < backup.sql
```

### Testing
```bash
# Run all tests
docker compose exec web python manage.py test

# Run specific app tests
docker compose exec web python manage.py test resumes
```

## Architecture Overview

### Core System
This is a **Resume Builder System** - a Django-based web application for creating and managing customized resumes for different job applications. The system is containerized with Docker.

### Key Components

1. **Django Application (`resumes` app)**
   - Main business logic for resume management
   - Personal information, experience, education, and skills models
   - Resume generation with company-specific customization
   - Multi-language support (Persian, English, German, French, Arabic)
   - PDF generation capabilities

2. **Database Layer**
   - MariaDB 11.4 for production/Docker
   - SQLite3 fallback for development (controlled by `USE_SQLITE` env var)
   - Full Persian/RTL text support with utf8mb4 encoding

3. **Service Architecture**
   - **Web Container**: Django application (internal port 8500)
   - **Database Container**: MariaDB (exposed on port 3307)
   - **Nginx Container**: Reverse proxy and static file serving (port 80)
   - **Management Tools**: Adminer (8085), phpMyAdmin (8086), Portainer (9000)

### Data Models Structure

**Core Models:**
- `PersonalInfo`: User's basic information, contact details, and default summary
- `Experience`: Work history with translation support
- `Education`: Academic background with translation support  
- `Skill`: Technical and soft skills categorized by type
- `JobSource`: Job posting sources (LinkedIn, Jobinja, etc.)

**Resume Management:**
- `Resume`: Central model linking personal info with job-specific customizations
- Supports resume copying/templating for different applications
- Company-specific summaries and salary expectations
- Job category-based skill filtering

**Translation Models:**
- `SkillTranslation`, `ExperienceTranslation`, `EducationTranslation`
- Support for multiple languages per resume

### Key Features

1. **Resume Customization**: Create tailored resumes for specific companies/roles
2. **Multi-language Support**: Generate resumes in different languages
3. **Smart Skill Filtering**: Automatically suggest relevant skills based on job category
4. **Resume Copying**: Duplicate existing resumes for similar applications
5. **PDF Generation**: Print-ready resume output
6. **Job Application Tracking**: Link resumes to specific job postings

### Development Database Configuration

The system supports both MariaDB (production) and SQLite (development):
- Set `USE_SQLITE=True` in environment for SQLite development
- Default MariaDB connection: `localhost:3307/resume_db`

### Persian/RTL Support

- Language code: `fa` (Persian)
- Timezone: `Asia/Tehran`
- TinyMCE editor configured for RTL text
- Database configured for utf8mb4 Persian text storage

### Static Files & Media

- Static files: Collected to `/app/static` via Docker volumes
- Media files: User uploads in `/app/media`
- Nginx serves both static and media files

### Testing Strategy

- Use Django's built-in test framework
- Test commands run inside Docker containers
- Focus on model relationships and view functionality