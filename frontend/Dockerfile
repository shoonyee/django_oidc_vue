# --- Builder Stage ---
  FROM node:20-alpine AS builder

  WORKDIR /app
  
  # Install dependencies 
  COPY package*.json ./
  RUN npm ci --only=production
  
  # Copy source code and build
  COPY . .
  RUN npm run build
  
  # --- Production Stage ---
  FROM nginx:alpine
  
  # Set environment variables for OpenShift detection
  ENV NGINX_PORT=8088
  
  # Copy built app to Nginx directory
  COPY --from=builder /app/dist /usr/share/nginx/html
  
  # Copy custom nginx configuration
  COPY nginx.conf /etc/nginx/nginx.conf
  
  # Ensure all necessary directories exist, set permissions for OpenShift's random UID/gid
  RUN mkdir -p /tmp/nginx /var/cache/nginx \
      && chmod -R g=u /usr/share/nginx/html /tmp/nginx /var/cache/nginx /tmp
  
  # Remove default Nginx site configs 
  RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/default.d/*
  
  # Expose non-privileged port for OpenShift
  EXPOSE 8088
  
  # Healthcheck for OpenShift/Kubernetes
  HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8088/health || exit 1
  
  # Start Nginx (do not specify USER; OpenShift sets this to a random non-root UID at runtime)
  CMD ["nginx", "-g", "daemon off;"]