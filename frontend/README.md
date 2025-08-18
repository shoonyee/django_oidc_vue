# Frontend Deployment Instructions

## Overview
This frontend is designed to be built locally and then packaged with nginx for OpenShift deployment.

## Prerequisites
- Node.js 22+ installed locally
- npm or yarn package manager
- Docker installed locally

## Build Process

### 1. Install Dependencies
```bash
npm install
```

### 2. Build Production Bundle
```bash
npm run build
```
This creates a `dist/` folder with optimized production files.

### 3. Verify Build Output
```bash
ls -la dist/
```
You should see:
- `index.html`
- `assets/` folder with JS/CSS files
- Other static assets

### 4. Build Docker Image
```bash
docker build -t your-app-frontend .
```

### 5. Test Locally (Optional)
```bash
docker run -d --name frontend-test -p 8088:8088 your-app-frontend
curl http://localhost:8088/health
# Should return "healthy"
```

## OpenShift Deployment

### 1. Tag and Push to Registry
```bash
# Tag for your OpenShift registry
docker tag your-app-frontend your-registry/your-namespace/your-app-frontend:latest

# Push to registry
docker push your-registry/your-namespace/your-app-frontend:latest
```

### 2. Deploy to OpenShift
Use the OpenShift console or CLI to deploy the image.

## Important Notes

- **Always run `npm run build` before building the Docker image**
- **The Dockerfile expects the `dist/` folder to exist**
- **No build process happens inside the container**
- **Container only serves pre-built static files with nginx**

## Troubleshooting

### Build Fails
- Ensure `dist/` folder exists after running `npm run build`
- Check that all dependencies are installed
- Verify Node.js version compatibility

### Container Won't Start
- Check that `dist/` folder was copied correctly
- Verify nginx configuration syntax
- Check OpenShift logs for permission issues

### Health Check Fails
- Ensure `/health` endpoint is accessible
- Check nginx is running inside container
- Verify port 8088 is exposed correctly

## File Structure
```
frontend/
├── Dockerfile          # OpenShift deployment
├── nginx.conf         # Nginx configuration
├── package.json       # Dependencies
├── src/               # Source code
├── dist/              # Built files (created by npm run build)
└── README.md          # This file
```
