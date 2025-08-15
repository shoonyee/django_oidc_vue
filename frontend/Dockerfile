# Multi-stage build for production deployment in OpenShift
FROM node:20-alpine AS builder

WORKDIR /app

# Install all dependencies (including dev dependencies needed for build)
COPY package*.json ./
RUN npm ci

# Copy source code and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Set environment variables for OpenShift
ENV NGINX_PORT=8088

# Copy built app to Nginx directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Ensure all necessary directories exist and set proper permissions
RUN mkdir -p /tmp/nginx /var/cache/nginx /var/log/nginx && \
    chown -R nginx:nginx /usr/share/nginx/html /tmp/nginx /var/cache/nginx /var/log/nginx /tmp && \
    chmod -R 755 /usr/share/nginx/html /tmp/nginx /var/cache/nginx /var/log/nginx

# Remove default Nginx site configs 
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/default.d/*

# Expose non-privileged port for OpenShift
EXPOSE 8088

# Healthcheck for OpenShift/Kubernetes
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8088/health || exit 1

# Switch to non-root user (nginx user already exists in nginx:alpine)
USER nginx

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]