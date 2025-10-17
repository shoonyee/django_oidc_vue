# Full Stack Application with Django + Vue.js

A modern full-stack web application featuring a Django backend with OIDC authentication via U-M Shibboleth and a Vue 3 frontend with Vuetify.

Decoupled implementation with separate backend and frontend containers.

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
├── backend/                    # Django backend application
│   ├── backend/               # Django project settings
│   ├── api/                   # API app with models and views
│   ├── Dockerfile             # Production deployment to OpenShift
│   ├── dockercompose/         # Local development with Docker Compose
│   │   ├── Dockerfile         # Development Dockerfile
│   │   └── docker-compose.yml # Docker Compose configuration
│   ├── manage.py              # Django management script
│   ├── .env                   # Environment configuration (database, OIDC, etc.)
│   └── requirements.txt       # Python dependencies
├── frontend/                  # Vue.js frontend application
│   ├── src/                   # Source code
│   │   ├── views/             # Vue components
│   │   ├── stores/            # Pinia state management
│   │   └── router/            # Vue Router configuration
│   ├── Dockerfile             # Production deployment to OpenShift
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
├── start.sh                   # Start both backend and frontend for local development
├── stop.sh                    # Stop both backend and frontend
└── README.md                  # This file
```

## Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **Docker and Docker Compose** (for containerized development)
- **External MySQL or PostgreSQL database server**
- **Access to U-M Shibboleth** (for OIDC authentication in production)

## Local Development

### Option 1: Using Start/Stop Scripts (Recommended)

The easiest way to run both backend and frontend for local development:

```bash
# Start both backend (Docker Compose) and frontend (npm dev server)
./start.sh

# Access the application:
# - Frontend: http://localhost:8088
# - Backend API: http://localhost:8080

# Stop all services
./stop.sh
```

**What `start.sh` does:**
1. Starts backend using Docker Compose from `backend/dockercompose/`
2. Runs database migrations automatically
3. Starts frontend using `npm run dev` on port 8088

**What `stop.sh` does:**
1. Stops backend Docker Compose services
2. Stops frontend npm dev server

### Option 2: Using Docker Compose Manually

```bash
# Start backend
cd backend/dockercompose
docker compose up -d

# In another terminal, start frontend
cd frontend
npm install  # First time only
npm run dev
```

### Option 3: Native Development (Without Docker)

#### Backend Setup

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
   # Edit .env with your database and OIDC configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start Django server:**
   ```bash
   python manage.py runserver 0.0.0.0:8080
   ```

#### Frontend Setup

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

The frontend will be available at `http://localhost:8088`

## Database Configuration

The application connects to external MySQL or PostgreSQL databases. Configure your connection in `backend/.env`.

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

### Complete .env File Structure

Create `backend/.env` with the following:

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

**Important Notes:**
- The application connects to **external databases only** - no local database files are created
- Ensure your database server allows connections from your application server
- Use `MODE=LOCAL` for development (bypasses OIDC and uses mock authentication)

## OpenShift Deployment

This project can be deployed to OpenShift directly from the GitHub repository. Since both backend and frontend are in the same repository but in different subdirectories, they need to be deployed as **two separate apps**.

### Prerequisites

1. **OpenShift CLI**: Install `oc` command-line tool
2. **GitHub Repository**: Clone or fork https://github.com/shoonyee/django_oidc_vue.git
3. **SSH Deploy Key**: For private repositories
4. **External Database**: MySQL or PostgreSQL accessible from OpenShift
5. **Project Access**: Access to an OpenShift project/namespace

### Step 1: Set Up SSH Authentication (For Private Repositories)

If your repository is private, set up SSH authentication:

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -f django-oidc-vue-key

# Add the public key (django-oidc-vue-key.pub) as a Deploy Key to your GitHub repository:
# Go to: GitHub Repository → Settings → Deploy keys → Add deploy key
# Copy contents of django-oidc-vue-key.pub

# Add the private key to OpenShift as a secret
oc create secret generic django-oidc-vue-ssh-key \
  --from-file=ssh-privatekey=./django-oidc-vue-key \
  --type=kubernetes.io/ssh-auth
```

### Step 2: Switch to Your OpenShift Project

```bash
# Switch to your project
oc project your-project-name

# Or create a new project
oc new-project your-project-name
```

### Step 3: Deploy Backend

The backend is in the `backend/` subdirectory and uses the `backend/Dockerfile`.

```bash
# Create backend app from subdirectory
oc new-app https://github.com/shoonyee/django_oidc_vue.git \
  --context-dir=backend \
  --name=app-backend \
  --strategy=docker

# For private repositories, use SSH URL
oc new-app git@github.com:shoonyee/django_oidc_vue.git \
  --context-dir=backend \
  --name=app-backend \
  --strategy=docker
```

**Configure the build to use SSH key (for private repos):**

```bash
# Edit the BuildConfig
oc edit bc/app-backend

# Update the source section to include the SSH secret:
# source:
#   git:
#     uri: 'git@github.com:shoonyee/django_oidc_vue.git'
#   sourceSecret:
#     name: django-oidc-vue-ssh-key
#   type: Git
#   contextDir: backend

# Start a new build
oc start-build app-backend
```

**Configure environment variables for database:**

```bash
# Set database configuration
oc set env deployment/app-backend \
  DB_ENGINE=mysql \
  DB_NAME=your_database_name \
  DB_USER=your_database_user \
  DB_PASSWORD=your_database_password \
  DB_HOST=your_database_host \
  DB_PORT=3306 \
  MODE=PROD \
  SECRET_KEY=your-secret-key-here \
  DEBUG=False

# Set OIDC configuration
oc set env deployment/app-backend \
  OIDC_CLIENT_ID=your-client-id \
  OIDC_CLIENT_SECRET=your-client-secret \
  OIDC_AUTHORIZATION_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/authorize \
  OIDC_TOKEN_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/token \
  OIDC_USER_ENDPOINT=https://shibboleth.umich.edu/idp/profile/oidc/userinfo \
  OIDC_JWKS_ENDPOINT=https://shibboleth.umich.edu/oidc/keyset.jwk

# Set CORS origins (update with your actual frontend URL after deployment)
oc set env deployment/app-backend \
  CORS_ALLOWED_ORIGINS=https://your-frontend-route.apps.openshift.com,https://your-backend-route.apps.openshift.com
```

**Create a route to expose backend:**

```bash
# Create route for backend
oc expose service/app-backend

# Get the backend URL
oc get route app-backend
```

### Step 4: Deploy Frontend

The frontend is in the `frontend/` subdirectory. **Important:** The frontend must be built locally first, then the built files deployed.

#### Option A: Build Locally and Deploy (Recommended)

```bash
# Clone the repository locally
git clone https://github.com/shoonyee/django_oidc_vue.git
cd django_oidc_vue/frontend

# Update vite.config.js with backend URL
# Edit vite.config.js and update the proxy target to your OpenShift backend URL
# Or for production, update API base URL to point to backend route

# Build production bundle
npm install
npm run build

# Create a new app from the current directory with built files
cd ..
oc new-app frontend/ \
  --name=app-frontend \
  --strategy=docker
```

#### Option B: Deploy from GitHub (Advanced)

For automated builds from GitHub, you need a custom build process since the frontend requires `npm run build`:

```bash
# Create frontend app from subdirectory
oc new-app https://github.com/shoonyee/django_oidc_vue.git \
  --context-dir=frontend \
  --name=app-frontend \
  --strategy=docker

# For private repositories
oc new-app git@github.com:shoonyee/django_oidc_vue.git \
  --context-dir=frontend \
  --name=app-frontend \
  --strategy=docker

# Configure SSH key for private repos
oc edit bc/app-frontend
# Add sourceSecret as shown in backend section
```

**Note:** This requires the `dist/` folder to be committed to the repository, which is not recommended. Use Option A for production deployments.

**Create a route to expose frontend:**

```bash
# Create route for frontend
oc expose service/app-frontend

# Get the frontend URL
oc get route app-frontend
```

### Step 5: Update Frontend Configuration

After deploying both apps, update the frontend to point to the correct backend URL:

```bash
# Get backend route URL
BACKEND_URL=$(oc get route app-backend -o jsonpath='{.spec.host}')
echo "Backend URL: https://$BACKEND_URL"

# Update frontend environment variable or rebuild with correct backend URL
# You may need to update vite.config.js locally and redeploy
```

### Step 6: Update Backend CORS Settings

Update the backend's CORS allowed origins to include the frontend URL:

```bash
# Get frontend route URL
FRONTEND_URL=$(oc get route app-frontend -o jsonpath='{.spec.host}')

# Update backend CORS settings
oc set env deployment/app-backend \
  CORS_ALLOWED_ORIGINS=https://$FRONTEND_URL,https://$BACKEND_URL
```

### Step 7: Run Database Migrations

```bash
# Run migrations in backend pod
oc get pods | grep app-backend
oc rsh <backend-pod-name>
python manage.py migrate
exit
```

### Complete Deployment Workflow

Here's a complete example deploying both apps:

```bash
# 1. Set up project
oc project your-project-name

# 2. Deploy backend from GitHub subdirectory
oc new-app https://github.com/shoonyee/django_oidc_vue.git \
  --context-dir=backend \
  --name=app-backend \
  --strategy=docker

# 3. Configure backend environment
oc set env deployment/app-backend \
  DB_ENGINE=mysql \
  DB_NAME=your_db \
  DB_USER=your_user \
  DB_PASSWORD=your_password \
  DB_HOST=your_db_host \
  DB_PORT=3306 \
  MODE=PROD \
  SECRET_KEY=$(openssl rand -base64 32) \
  DEBUG=False

# 4. Expose backend
oc expose service/app-backend

# 5. Build frontend locally
git clone https://github.com/shoonyee/django_oidc_vue.git
cd django_oidc_vue/frontend
npm install
npm run build

# 6. Update frontend config with backend URL
BACKEND_URL=$(oc get route app-backend -o jsonpath='{.spec.host}')
# Update vite.config.js or environment config with backend URL

# 7. Deploy frontend
cd ..
oc new-app frontend/ --name=app-frontend --strategy=docker

# 8. Expose frontend
oc expose service/app-frontend

# 9. Get URLs
echo "Frontend: https://$(oc get route app-frontend -o jsonpath='{.spec.host}')"
echo "Backend: https://$(oc get route app-backend -o jsonpath='{.spec.host}')"

# 10. Update backend CORS
oc set env deployment/app-backend \
  CORS_ALLOWED_ORIGINS=https://$(oc get route app-frontend -o jsonpath='{.spec.host}')

# 11. Run migrations
oc rsh $(oc get pods -l app=app-backend -o name | head -1)
python manage.py migrate
exit
```

### Monitoring and Troubleshooting

```bash
# View backend logs
oc logs -f deployment/app-backend

# View frontend logs
oc logs -f deployment/app-frontend

# Check pod status
oc get pods

# Describe pod for issues
oc describe pod <pod-name>

# Access backend shell
oc rsh <backend-pod-name>

# Check build logs
oc logs -f bc/app-backend
oc logs -f bc/app-frontend

# Trigger rebuild
oc start-build app-backend
oc start-build app-frontend
```

### Important Configuration Notes

1. **Backend Environment Variables**: Must be set in OpenShift, not in `.env` file
2. **Frontend API URL**: Update `vite.config.js` to point to OpenShift backend route
3. **Database Connection**: Backend must be able to reach external database
4. **CORS Settings**: Must include both frontend and backend URLs
5. **HTTPS**: OpenShift routes use HTTPS by default
6. **Build Context**: Use `--context-dir` to specify subdirectory for each app

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

### Development Mode (MODE=LOCAL)

For local development, set `MODE=LOCAL` in your `.env` file to use mock authentication:
- No OIDC redirects
- Mock user is automatically authenticated
- Bypasses U-M Shibboleth for local testing

### Production Mode (MODE=PROD)

In production, set `MODE=PROD` and configure OIDC credentials:
1. **No Custom Login**: The frontend has no login forms
2. **Automatic Redirects**: Users are sent to U-M Shibboleth for authentication
3. **Seamless Integration**: After U-M authentication, users return to the app
4. **Session Management**: Django handles OIDC sessions automatically

### U-M Shibboleth Configuration

The application uses U-M's OIDC endpoints from [https://shibboleth.umich.edu/.well-known/openid-configuration](https://shibboleth.umich.edu/.well-known/openid-configuration)

**Note**: You'll need to register your application with U-M IT to obtain the client ID and secret.

## Development

### Backend Development

- Django REST Framework for API endpoints
- Models defined in `backend/api/models.py`
- Views and serializers in `backend/api/views.py` and `backend/api/serializers.py`
- Admin interface at `/admin/` for data management
- OIDC authentication handled by `mozilla-django-oidc`
- Database connections configured via environment variables

### Frontend Development

- Built with Vue 3 Composition API
- Vuetify 3 for Material Design components
- State management with Pinia
- Routing with Vue Router 4
- HTTP requests with Axios
- Vite proxy for API calls during development

## Troubleshooting

### Backend Issues

**Database Connection Errors:**
- Check `backend/.env` file for correct database credentials
- Verify network access to database server
- Ensure database port is accessible
- Check database user permissions

**Docker Compose Issues:**
- Port conflicts: Run `docker compose down` first
- Permission errors: Check file permissions on Docker volumes
- Container won't start: Check logs with `docker compose logs`

### Frontend Issues

**Port 8088 Already in Use:**
- Stop other processes: `pkill -f "npm run dev"`
- Check Docker containers: `docker ps`

**Axios 500 Errors:**
- Verify backend is running on port 8080
- Check backend logs for errors
- Verify database connection

**Build Errors:**
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`

### Start/Stop Script Issues

**Backend won't start:**
- Ensure Docker Compose is running: `docker compose ps`
- Check backend logs: `cd backend/dockercompose && docker compose logs`

**Frontend won't start:**
- Check for port conflicts on 8088
- Verify `node_modules` exists: `cd frontend && npm install`

## Summary

### Local Development vs OpenShift Deployment

| Purpose | Backend | Frontend |
|---------|---------|----------|
| **Local Development (Scripts)** | Use `./start.sh` | Use `./start.sh` |
| **Local Development (Manual)** | `cd backend/dockercompose && docker compose up` | `cd frontend && npm run dev` |
| **OpenShift Deployment** | `oc new-app` with `--context-dir=backend` | Build locally → `oc new-app frontend/` |

### Key Differences

#### Local Development
- **Backend**: Uses `backend/dockercompose/Dockerfile` and `docker-compose.yml`
- **Frontend**: Runs directly with `npm run dev` (port 8088)
- **Database**: Connect to external database via `backend/.env`
- **Hot Reload**: Enabled for both backend and frontend
- **Authentication**: Use `MODE=LOCAL` for mock authentication

#### OpenShift Deployment
- **Backend**: Uses `backend/Dockerfile` with `oc new-app` and `--context-dir=backend`
- **Frontend**: Build locally first (`npm run build`), then deploy with `oc new-app frontend/`
- **Database**: Configure via `oc set env deployment/app-backend`
- **Repository Structure**: Deploy from subdirectories of same GitHub repo
- **SSH Authentication**: Required for private repositories
- **Routes**: Expose both apps with `oc expose service`
- **CORS**: Update backend to include frontend route URL
- **Configuration**: Frontend must be updated with backend route URL

### Quick Command Reference

```bash
# Local Development
./start.sh                          # Start both services
./stop.sh                           # Stop both services

# OpenShift Deployment
oc new-app https://github.com/shoonyee/django_oidc_vue.git \
  --context-dir=backend --name=app-backend --strategy=docker

oc new-app frontend/ --name=app-frontend --strategy=docker

# Configuration
oc set env deployment/app-backend DB_HOST=... DB_NAME=...
oc expose service/app-backend
oc expose service/app-frontend
```

## Support

For issues related to:
- **Database connectivity**: Check your `.env` configuration and network access
- **OIDC authentication**: Contact U-M IT for Shibboleth configuration
- **Docker/OpenShift**: Review container logs and configurations
- **Application functionality**: Check API documentation and application logs
