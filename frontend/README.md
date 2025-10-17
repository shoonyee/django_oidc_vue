# Frontend - Vue.js Application

Vue 3 frontend with Vuetify for the Full Stack Application.

## Overview

This frontend is designed for:
- **Local Development**: Run with `npm run dev` or via `../start.sh` script
- **OpenShift Deployment**: Build locally first, then deploy with Docker

## Local Development

### Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:8088`

### Using Project Scripts

From the project root:

```bash
# Start both backend and frontend
./start.sh

# Stop both services
./stop.sh
```

### Development Configuration

- **Port**: 8088 (configured in `vite.config.js`)
- **API Proxy**: Requests to `/api` and `/oidc` are proxied to backend at `http://host.docker.internal:8080`
- **Hot Reload**: Enabled for live code changes

## OpenShift Deployment

### Important: Local Build Required

The `Dockerfile` is designed for OpenShift deployment and requires the production build to be done **locally first**. The Dockerfile only packages the pre-built files with nginx.

### Quick Deployment

```bash
# 1. Clone and build locally
git clone https://github.com/shoonyee/django_oidc_vue.git
cd django_oidc_vue/frontend

# 2. Update vite.config.js with backend URL (or configure for production)
# Edit proxy settings to point to OpenShift backend route

# 3. Build production bundle
npm install
npm run build

# 4. Deploy to OpenShift from parent directory
cd ..
oc new-app frontend/ --name=app-frontend --strategy=docker

# 5. Expose frontend service
oc expose service/app-frontend

# 6. Get frontend URL
oc get route app-frontend
```

### Detailed Deployment Steps

#### 1. Update Frontend Configuration

Before building, update the API endpoint configuration:

**For production deployment**, you may need to update how the frontend calls the backend API. The backend URL will be the OpenShift route created for the backend.

#### 2. Build Production Bundle Locally

```bash
# Install dependencies (if not already done)
npm install

# Build production bundle
npm run build
```

This creates a `dist/` folder with optimized production files.

#### 3. Verify Build Output

```bash
ls -la dist/
```

You should see:
- `index.html`
- `assets/` folder with JS/CSS files
- Other static assets

#### 4. Deploy to OpenShift

**Option A: Deploy from local directory (Recommended)**

```bash
# From the project root directory
oc new-app frontend/ --name=app-frontend --strategy=docker

# Expose the service
oc expose service/app-frontend
```

**Option B: Deploy from GitHub (Advanced)**

**Note:** This requires the `dist/` folder to be committed to the repository.

```bash
# Deploy from GitHub subdirectory
oc new-app https://github.com/shoonyee/django_oidc_vue.git \
  --context-dir=frontend \
  --name=app-frontend \
  --strategy=docker

# For private repositories
oc new-app git@github.com:shoonyee/django_oidc_vue.git \
  --context-dir=frontend \
  --name=app-frontend \
  --strategy=docker

# Expose the service
oc expose service/app-frontend
```

**Option C: Using automated script**

```bash
chmod +x build-and-deploy.sh
./build-and-deploy.sh
```

The script will:
1. Check prerequisites (Node.js, npm, Docker)
2. Install dependencies if needed
3. Build production bundle
4. Create Docker image
5. Provide next steps for deployment

#### 5. Update Backend CORS Settings

After frontend deployment, update the backend to allow frontend URL:

```bash
# Get frontend URL
FRONTEND_URL=$(oc get route app-frontend -o jsonpath='{.spec.host}')

# Update backend CORS
oc set env deployment/app-backend \
  CORS_ALLOWED_ORIGINS=https://$FRONTEND_URL
```

### Test Locally Before OpenShift

```bash
# Run the production container locally
docker run -d --name frontend-test -p 8088:8088 app-frontend

# Test health endpoint
curl http://localhost:8088/health
# Should return "healthy"

# Test main page
curl http://localhost:8088/

# Clean up
docker stop frontend-test
docker rm frontend-test
```

### Monitoring in OpenShift

```bash
# View logs
oc logs -f deployment/app-frontend

# Check pod status
oc get pods -l app=app-frontend

# Describe pod
oc describe pod <frontend-pod-name>

# Access nginx shell
oc rsh <frontend-pod-name>
```

### Complete Deployment Example

See the main project README.md for a complete step-by-step deployment guide including both backend and frontend together.

## Project Structure

```
frontend/
├── src/
│   ├── main.js              # Application entry point
│   ├── App.vue              # Root component
│   ├── router/
│   │   └── index.js         # Vue Router configuration
│   ├── stores/
│   │   └── auth.js          # Pinia authentication store
│   └── views/
│       ├── Home.vue         # Home page
│       ├── Model1.vue       # Model1 management
│       ├── Model2.vue       # Model2 management
│       ├── Models.vue       # Models overview
│       └── Contact.vue      # Contact form
├── Dockerfile               # OpenShift deployment (requires local build)
├── nginx.conf               # Nginx configuration for production
├── vite.config.js           # Vite development server configuration
├── package.json             # Dependencies and scripts
├── build-and-deploy.sh      # Automated build script
└── README.md                # This file
```

## Configuration Files

### vite.config.js

Configures the development server:
- **Port**: 8088
- **API Proxy**: Routes `/api` and `/oidc` to backend
- **Build Output**: `dist/` directory

### nginx.conf

Production nginx configuration:
- **Port**: 8088 (non-privileged for OpenShift)
- **SPA Routing**: Serves `index.html` for all routes
- **Health Check**: `/health` endpoint
- **Static Assets**: Optimized caching
- **OpenShift Compatible**: Arbitrary UID support

### Dockerfile

Production container:
- **Base**: nginx:alpine
- **Expects**: Local `dist/` folder from `npm run build`
- **No Build**: Container only serves pre-built files
- **OpenShift Ready**: SCC compliant

## Important Notes

### Local Development vs Production

| Aspect | Local Development | Production (OpenShift) |
|--------|------------------|----------------------|
| **How to run** | `npm run dev` | Build locally → Docker |
| **Server** | Vite dev server | Nginx |
| **Port** | 8088 | 8088 |
| **Hot Reload** | Yes | No |
| **API Proxy** | Vite proxy | Nginx proxy (if needed) |
| **Build** | No build needed | Must run `npm run build` first |

### Dockerfile Requirements

- **Always run `npm run build` before building Docker image**
- **The Dockerfile expects the `dist/` folder to exist**
- **No build process happens inside the container**
- **Container only serves pre-built static files with nginx**

### OpenShift Considerations

- Container runs on port 8088 (non-privileged)
- Compatible with arbitrary UIDs (OpenShift SCC)
- Health check endpoint at `/health`
- Nginx configured for OpenShift temp directories

## Troubleshooting

### Local Development Issues

**Port 8088 already in use:**
```bash
# Find and kill process
lsof -ti:8088 | xargs kill -9

# Or kill all npm dev servers
pkill -f "npm run dev"
```

**API calls failing:**
- Verify backend is running on port 8080
- Check `vite.config.js` proxy configuration
- Look for CORS errors in browser console

**Dependencies issues:**
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### Build Issues

**Build fails:**
- Ensure all dependencies are installed: `npm install`
- Check Node.js version: `node --version` (should be 16+)
- Clear cache: `npm cache clean --force`

**dist/ folder not created:**
- Check for build errors in terminal
- Verify `package.json` has `"build": "vite build"` script
- Check disk space

### Docker Issues

**Docker build fails:**
```bash
# Ensure dist/ exists
ls -la dist/

# If not, build it first
npm run build

# Then build Docker image
docker build -t app-frontend .
```

**Container won't start:**
```bash
# Check logs
docker logs frontend-test

# Verify nginx config
docker exec frontend-test nginx -t
```

**Health check fails:**
- Container should serve nginx on port 8088
- `/health` endpoint should return "healthy"
- Check nginx logs for errors

### OpenShift Deployment Issues

**Permission errors:**
- Dockerfile is configured for arbitrary UIDs
- Check that temp directories use `/tmp/nginx`

**Container crashes:**
- Check OpenShift pod logs
- Verify nginx configuration syntax
- Ensure port 8088 is correctly exposed

**Files not found:**
- Verify `dist/` folder was built before Docker build
- Check `.dockerignore` doesn't exclude `dist/`

## Scripts

### package.json Scripts

```bash
# Development server with hot reload
npm run dev

# Build production bundle
npm run build

# Preview production build locally (requires build first)
npm run preview
```

### build-and-deploy.sh

Automated script that:
1. Checks prerequisites (Node.js, npm, Docker)
2. Installs dependencies if needed
3. Cleans previous build
4. Builds production bundle
5. Creates Docker image
6. Provides deployment instructions

Usage:
```bash
chmod +x build-and-deploy.sh
./build-and-deploy.sh
```

## Development Workflow

### Daily Development

```bash
# Start development
npm run dev

# Make changes
# Browser auto-refreshes with changes

# Test with backend
# Ensure backend is running on port 8080
```

### Preparing for Deployment

```bash
# Build production version
npm run build

# Test production build locally
npm run preview

# Build Docker image
docker build -t app-frontend .

# Test Docker image
docker run -d --name test -p 8088:8088 app-frontend
curl http://localhost:8088/health

# Push to registry and deploy
docker tag app-frontend your-registry/namespace/app-frontend:latest
docker push your-registry/namespace/app-frontend:latest
oc new-app your-registry/namespace/app-frontend:latest
```

## Summary

**For Local Development:**
- Use `npm run dev` or `../start.sh` from project root
- No Docker needed for development
- Hot reload enabled

**For OpenShift Deployment:**
1. Build locally: `npm run build`
2. Create Docker image: `docker build -t app-frontend .`
3. Deploy with: `oc new-app`

**Key Point:** The Dockerfile is for OpenShift production deployment only and requires local build first.
