# Backend - Django REST API

Django REST Framework backend with OIDC authentication for the Full Stack Application.

## Overview

This backend is designed for:
- **Local Development**: Run with Docker Compose or via `../start.sh` script
- **OpenShift Deployment**: Deploy with `Dockerfile` using `oc new-app`

## Local Development

### Quick Start with Docker Compose

```bash
# From backend/dockercompose directory
cd dockercompose
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

The API will be available at `http://localhost:8080`

### Using Project Scripts

From the project root:

```bash
# Start both backend and frontend
./start.sh

# Stop both services
./stop.sh
```

### Native Development (Without Docker)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your database and OIDC configuration

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver 0.0.0.0:8080
```

## Database Configuration

The backend connects to **external MySQL or PostgreSQL databases only**. No local database files are created.

### Configure .env File

Create a `backend/.env` file:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Application Mode
MODE=LOCAL  # Use LOCAL for development with mock auth, PROD for production with OIDC

# Database Configuration - Choose ONE database engine
DB_ENGINE=mysql  # or postgresql
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_database_server_host
DB_PORT=3306  # 3306 for MySQL, 5432 for PostgreSQL

# OIDC Authentication Settings (only used when MODE=PROD)
OIDC_CLIENT_ID=your-app-client-id
OIDC_CLIENT_SECRET=your-app-client-secret

# U-M Shibboleth OIDC endpoints
OIDC_AUTHORIZATION_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/authorize
OIDC_TOKEN_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/token
OIDC_USER_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/userinfo
OIDC_JWKS_ENDPOINT=https://shibboleth.umich.edu/oidc/keyset.jwk

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:8088,http://127.0.0.1:8088,http://localhost:8080,http://127.0.0.1:8080

# Email Configuration
DEFAULT_FROM_EMAIL=noreply@example.com
ADMIN_EMAILS=admin@example.com
```

### MySQL Configuration

```bash
DB_ENGINE=mysql
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_mysql_server_host
DB_PORT=3306
```

**Required**: `PyMySQL` package (included in `requirements.txt`)

### PostgreSQL Configuration

```bash
DB_ENGINE=postgresql
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_postgresql_server_host
DB_PORT=5432
```

**Required**: `psycopg2-binary` package (included in `requirements.txt`)

## Project Structure

```
backend/
├── api/                        # Main API application
│   ├── models.py              # Database models (Model1, Model2)
│   ├── views.py               # API views and endpoints
│   ├── serializers.py         # DRF serializers
│   ├── admin.py               # Django admin configuration
│   └── migrations/            # Database migrations
├── backend/                   # Django project settings
│   ├── settings.py            # Main settings file
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI configuration
├── dockercompose/             # Local development Docker setup
│   ├── Dockerfile             # Development Dockerfile
│   └── docker-compose.yml     # Docker Compose configuration
├── Dockerfile                 # OpenShift production deployment
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration (not in git)
└── env.example                # Example environment configuration
```

## Docker Compose (Local Development)

### Configuration

- **Port**: 8080
- **Hot Reload**: Enabled via volume mounting
- **Database**: Connects to external database via `.env`
- **Migrations**: Run automatically on startup

### Files

- `dockercompose/Dockerfile` - Development Dockerfile with hot reload
- `dockercompose/docker-compose.yml` - Service configuration

### Usage

```bash
cd dockercompose

# Start services
docker compose up -d

# View logs
docker compose logs -f backend

# Run migrations
docker compose exec backend python manage.py migrate

# Create superuser
docker compose exec backend python manage.py createsuperuser

# Access Django shell
docker compose exec backend python manage.py shell

# Stop services
docker compose down
```

## OpenShift Deployment

### Deploying from GitHub Repository

The backend is in a subdirectory of the repository, so you need to use `--context-dir`:

```bash
# Switch to your OpenShift project
oc project your-project-name

# Deploy backend from GitHub subdirectory
oc new-app https://github.com/shoonyee/django_oidc_vue.git \
  --context-dir=backend \
  --name=app-backend \
  --strategy=docker

# For private repositories, use SSH
oc new-app git@github.com:shoonyee/django_oidc_vue.git \
  --context-dir=backend \
  --name=app-backend \
  --strategy=docker
```

### Configure Environment Variables

Set database and application configuration in OpenShift:

```bash
# Database configuration
oc set env deployment/app-backend \
  DB_ENGINE=mysql \
  DB_NAME=your_database_name \
  DB_USER=your_database_user \
  DB_PASSWORD=your_database_password \
  DB_HOST=your_database_host \
  DB_PORT=3306 \
  MODE=PROD \
  SECRET_KEY=$(openssl rand -base64 32) \
  DEBUG=False

# OIDC configuration
oc set env deployment/app-backend \
  OIDC_CLIENT_ID=your-client-id \
  OIDC_CLIENT_SECRET=your-client-secret

# CORS (update with your frontend URL after deployment)
oc set env deployment/app-backend \
  CORS_ALLOWED_ORIGINS=https://your-frontend-url
```

### Expose Backend Service

```bash
# Create route
oc expose service/app-backend

# Get backend URL
oc get route app-backend
```

### Run Database Migrations

```bash
# Access backend pod
oc rsh $(oc get pods -l app=app-backend -o name | head -1)

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

exit
```

### Production Dockerfile Features

The `backend/Dockerfile`:
- Uses multi-stage build for smaller image
- Installs only production dependencies
- Runs as non-root user
- Uses Gunicorn as WSGI server
- Includes health check endpoint
- Compatible with OpenShift Security Context Constraints (SCC)
- Connects to external database only

### Important Notes

- **Do not use** `backend/Dockerfile` for local development
- Use `backend/dockercompose/` for local development
- Production Dockerfile does not include development tools
- Environment variables must be configured in OpenShift (not `.env` file)
- Database must be accessible from OpenShift pods
- Update CORS settings with actual frontend URL after deployment

### Complete Deployment Example

See the main project README.md for a complete step-by-step deployment guide including both backend and frontend.

## API Endpoints

### Public Endpoints (No Authentication)

```
GET  /api/public/health_check/  - Health check
GET  /api/public/public_info/   - Application information
POST /api/contact/              - Submit contact form
```

### Protected Endpoints (Authentication Required)

#### Model1 Endpoints
```
GET    /api/model1/        - List all Model1 entries
POST   /api/model1/        - Create new Model1 entry
GET    /api/model1/{id}/   - Retrieve Model1 entry
PUT    /api/model1/{id}/   - Update Model1 entry
DELETE /api/model1/{id}/   - Delete Model1 entry
```

#### Model2 Endpoints
```
GET    /api/model2/                  - List all Model2 entries
POST   /api/model2/                  - Create new Model2 entry
GET    /api/model2/{id}/             - Retrieve Model2 entry
PUT    /api/model2/{id}/             - Update Model2 entry
DELETE /api/model2/{id}/             - Delete Model2 entry
POST   /api/model2/{id}/toggle_active/ - Toggle active status
```

### Authentication Endpoints
```
GET /api/auth/user/         - Get current user information
GET /oidc/authenticate/     - Redirect to U-M OIDC login
GET /oidc/callback/         - OIDC callback endpoint
GET /oidc/logout/           - Logout and redirect
```

## Authentication

### Development Mode (MODE=LOCAL)

For local development without OIDC:

```bash
# In .env
MODE=LOCAL
```

This enables:
- Mock authentication bypass
- No OIDC redirects
- Automatic test user creation
- Faster development iteration

### Production Mode (MODE=PROD)

For production with U-M Shibboleth OIDC:

```bash
# In .env
MODE=PROD
OIDC_CLIENT_ID=your-client-id
OIDC_CLIENT_SECRET=your-client-secret
```

This enables:
- Full OIDC authentication flow
- U-M Shibboleth integration
- Secure session management
- User profile from U-M

**Note**: Contact U-M IT to register your application and obtain OIDC credentials.

## Database Migrations

### Create Migrations

```bash
# Native
python manage.py makemigrations

# Docker Compose
docker compose exec backend python manage.py makemigrations
```

### Apply Migrations

```bash
# Native
python manage.py migrate

# Docker Compose
docker compose exec backend python manage.py migrate
```

### View Migrations

```bash
# Native
python manage.py showmigrations

# Docker Compose
docker compose exec backend python manage.py showmigrations
```

## Admin Interface

Django admin is available at `/admin/`

### Create Superuser

```bash
# Native
python manage.py createsuperuser

# Docker Compose
docker compose exec backend python manage.py createsuperuser
```

Access at: `http://localhost:8080/admin/`

## Development

### Models

Models are defined in `api/models.py`:
- **Model1**: Basic model with text and date fields
- **Model2**: Model with active status toggle and relations

### Views

API views in `api/views.py`:
- Django REST Framework ViewSets
- Custom actions (e.g., `toggle_active`)
- Permission classes for authentication

### Serializers

Data serializers in `api/serializers.py`:
- Model serialization
- Validation logic
- Custom fields

### Settings

Configuration in `backend/settings.py`:
- Database configuration via `decouple`
- OIDC authentication setup
- CORS and CSRF settings
- Middleware configuration

## Troubleshooting

### Database Connection Issues

**Cannot connect to database:**
```bash
# Check .env configuration
cat .env

# Test database connection
docker compose exec backend python manage.py dbshell

# Or check with Django shell
docker compose exec backend python manage.py shell
>>> from django.db import connection
>>> connection.cursor()
```

**Common issues:**
- Wrong database credentials in `.env`
- Database server not accessible
- Port not open/accessible
- SSL requirements not met

### Docker Compose Issues

**Port 8080 already in use:**
```bash
# Stop all containers
docker compose down

# Or find and stop conflicting service
lsof -ti:8080 | xargs kill -9
```

**Container won't start:**
```bash
# Check logs
docker compose logs backend

# Rebuild container
docker compose down
docker compose build --no-cache
docker compose up -d
```

**Permission errors:**
```bash
# Check volume permissions
ls -la ./

# Rebuild with fresh volumes
docker compose down -v
docker compose up -d
```

### Migration Issues

**Migrations not applied:**
```bash
# Check migration status
docker compose exec backend python manage.py showmigrations

# Apply migrations
docker compose exec backend python manage.py migrate

# If issues persist, check database connectivity
```

**Conflicting migrations:**
```bash
# Reset migrations (development only!)
docker compose exec backend python manage.py migrate api zero
docker compose exec backend python manage.py migrate
```

### OIDC Authentication Issues

**Redirect loop:**
- Check `MODE` setting in `.env`
- Verify OIDC credentials
- Check CORS and CSRF settings

**Cannot access protected endpoints:**
- Verify authentication is working: `GET /api/auth/user/`
- Check browser cookies
- Review OIDC callback logs

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | Yes | Debug mode (True/False) |
| `MODE` | Yes | Application mode (LOCAL/PROD) |
| `DB_ENGINE` | Yes | Database engine (mysql/postgresql) |
| `DB_NAME` | Yes | Database name |
| `DB_USER` | Yes | Database username |
| `DB_PASSWORD` | Yes | Database password |
| `DB_HOST` | Yes | Database host |
| `DB_PORT` | Yes | Database port |
| `OIDC_CLIENT_ID` | PROD only | OIDC client ID |
| `OIDC_CLIENT_SECRET` | PROD only | OIDC client secret |
| `CORS_ALLOWED_ORIGINS` | Yes | Allowed CORS origins |
| `DEFAULT_FROM_EMAIL` | Optional | Email from address |
| `ADMIN_EMAILS` | Optional | Admin email addresses |

## Summary

| Purpose | Configuration | How to Run |
|---------|--------------|------------|
| **Local Development** | `dockercompose/` | `cd dockercompose && docker compose up` |
| **Local with Scripts** | `dockercompose/` | `../start.sh` from project root |
| **Native Development** | `.env` + venv | `python manage.py runserver 0.0.0.0:8080` |
| **OpenShift Deployment** | `Dockerfile` | `oc new-app . --strategy=docker` |

**Key Points:**
- Use `dockercompose/` for local development with hot reload
- Use `Dockerfile` only for OpenShift production deployment
- Always configure external database in `.env`
- Use `MODE=LOCAL` for development, `MODE=PROD` for production

