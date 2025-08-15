# Full Stack Application with Django + Vue.js

A modern full-stack web application featuring a Django backend with OIDC authentication via U-M Shibboleth and a Vue 3 frontend with Vuetify.

Decoupled implementation

## Features

- **Backend**: Django REST API with OIDC authentication
- **Frontend**: Vue 3 + Vuetify with responsive design
- **Authentication**: OIDC integration with University of Michigan Shibboleth
- **Models**: Two sample models (Model1, Model2) with CRUD operations
- **Contact Form**: Public contact form (no authentication required)
- **Responsive Design**: Mobile-friendly interface
- **Database Support**: External MySQL or PostgreSQL databases

## Project Structure

```
├── backend/                 # Django backend application
│   ├── backend/            # Django project settings
│   ├── api/                # API app with models and views
│   ├── manage.py           # Django management script
│   ├── .env                # Environment configuration (database, OIDC, etc.)
│   └── requirements.txt    # Python dependencies
├── frontend/               # Vue.js frontend application
│   ├── src/                # Source code
│   │   ├── views/          # Vue components
│   │   ├── stores/         # Pinia state management
│   │   └── router/         # Vue Router configuration
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Docker and Docker Compose
- Access to U-M Shibboleth (for OIDC authentication)
- External MySQL or PostgreSQL database server

## Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your database and U-M OIDC configuration
   ```

5. **Configure external database connection** (see Database Configuration section below)

6. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## Database Configuration

The application supports connecting to external MySQL or PostgreSQL databases. Configure your database connection in the `backend/.env` file.

### MySQL Configuration

```bash
# Database Configuration - External MySQL Server
DB_ENGINE=mysql
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_mysql_server_host
DB_PORT=3306
```

**Required Dependencies**: The `requirements.txt` includes `PyMySQL` for MySQL connectivity.

### PostgreSQL Configuration

```bash
# Database Configuration - External PostgreSQL Server
DB_ENGINE=postgresql
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_postgresql_server_host
DB_PORT=5432
```

**Required Dependencies**: The `requirements.txt` includes `psycopg2-binary` for PostgreSQL connectivity.

### Environment Variables

Create a `backend/.env` file with the following structure:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Application Mode
MODE=LOCAL  # or PROD for production with OIDC

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
ADMIN_EMAILS=admin@example.com,admin2@example.com
```

### Database Connection Notes

- **External Database Only**: The application connects to existing external databases, it does not create local database files
- **No SQLite**: For production use, always use external MySQL or PostgreSQL
- **Connection Security**: Ensure your database server allows connections from your application server
- **Environment Isolation**: Use different `.env` files for different environments (development, staging, production)

## Docker Deployment

### Using Docker Compose

1. **Start backend with external database:**
   ```bash
   cd backend/dockercompose
   docker compose up -d
   ```

2. **Start frontend with npm:**
   ```bash
   cd frontend
   npm run dev
   ```

### Using Start Scripts

```bash
# Start all services
./start.sh

# Stop all services
./stop.sh
```

## API Endpoints

### Public Endpoints (No Authentication Required)
- `GET /api/public/health_check/` - Health check
- `GET /api/public/public_info/` - Application information
- `POST /api/contact/` - Submit contact form

### Protected Endpoints (Authentication Required)
- `GET /api/model1/` - List Model1 entries
- `POST /api/model1/` - Create Model1 entry
- `PUT /api/model1/{id}/` - Update Model1 entry
- `DELETE /api/model1/{id}/` - Delete Model1 entry
- `GET /api/model2/` - List Model2 entries
- `POST /api/model2/` - Create Model2 entry
- `PUT /api/model2/{id}/` - Update Model2 entry
- `DELETE /api/model2/{id}/` - Delete Model2 entry
- `POST /api/model2/{id}/toggle_active/` - Toggle Model2 active status

### Authentication Endpoints
- `GET /api/auth/user/` - Get current user information
- `GET /oidc/authenticate/` - Redirect to U-M OIDC login
- `GET /oidc/logout/` - Redirect to U-M OIDC logout

## Authentication

The application uses OIDC (OpenID Connect) authentication with U-M Shibboleth. **There is no custom login interface** - users are automatically redirected to U-M's official login page when authentication is required.

### How It Works

1. **No Custom Login**: The frontend has no login forms or custom authentication
2. **Automatic Redirects**: When accessing protected routes, users are automatically sent to U-M Shibboleth
3. **Seamless Integration**: After successful U-M authentication, users are redirected back to the app
4. **Session Management**: Django handles OIDC sessions automatically

### U-M Shibboleth OIDC Configuration

The application is configured to work with U-M's official OIDC endpoints from [https://shibboleth.umich.edu/.well-known/openid-configuration](https://shibboleth.umich.edu/.well-known/openid-configuration):

### Supported Scopes and Claims

Based on U-M's OIDC configuration, the application supports:
- **Scopes**: `openid`, `email`, `profile`, `eduperson`, `edumember`
- **Claims**: Standard OIDC claims plus U-M specific attributes like `eduperson_principal_name`, `eduperson_affiliation`, `edumember_is_member_of`

### Configuration

Update the following environment variables in `backend/.env`:

**Note**: You'll need to register your application with U-M IT to obtain the client ID and secret.

**.env**, you can set **MODE** to **LOCAL** to use a mocked user for local development.

## Development

### Backend Development

- The Django backend uses Django REST Framework for API endpoints
- Models are defined in `backend/api/models.py`
- Views and serializers are in `backend/api/views.py` and `backend/api/serializers.py`
- Admin interface is available at `/admin/` for data management
- OIDC authentication is handled by `mozilla-django-oidc`
- Database connections are configured via environment variables

### Frontend Development

- Built with Vue 3 Composition API
- Uses Vuetify 3 for Material Design components
- State management with Pinia
- Routing with Vue Router 4
- HTTP requests with Axios
- Automatic OIDC redirects for authentication

## Deployment

### Backend Deployment

1. Set `DEBUG=False` in production
2. Use external production database (MySQL or PostgreSQL)
3. Configure static files with WhiteNoise
4. Set up proper CORS settings for production domains
5. Ensure HTTPS is enabled for OIDC security
6. Use production-grade database credentials

### Frontend Deployment

1. Build the production version:
   ```bash
   npm run build
   ```
2. Deploy the `dist/` folder to your web server
3. Configure API proxy settings for production

### Database Deployment Considerations

- **Connection Security**: Use SSL/TLS connections to production databases
- **Connection Pooling**: Configure appropriate connection pool sizes
- **Backup Strategy**: Ensure your external database has proper backup procedures
- **Monitoring**: Monitor database connection health and performance
- **Scaling**: Plan for database scaling as your application grows

## Troubleshooting

### Database Connection Issues

1. **Check .env file**: Ensure all database variables are set correctly
2. **Verify network access**: Confirm your application server can reach the database server
3. **Check credentials**: Verify username, password, and database name
4. **Port accessibility**: Ensure the database port is open and accessible
5. **SSL requirements**: Some databases require SSL connections

### Common Issues

- **"No module named 'pymysql'"**: Install MySQL dependencies with `pip install -r requirements.txt`
- **"No module named 'psycopg2'"**: Install PostgreSQL dependencies with `pip install -r requirements.txt`
- **Connection refused**: Check database server status and network connectivity
- **Authentication failed**: Verify database credentials and user permissions

## Support

For issues related to:
- **Database connectivity**: Check your `.env` configuration and network access
- **OIDC authentication**: Contact U-M IT for Shibboleth configuration
- **Application functionality**: Review the API documentation and check logs
