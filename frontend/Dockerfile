FROM node:22-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

# Copy source code and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Set environment variables for OpenShift
ENV NGINX_PORT=8088

# Install wget for health checks
RUN apk add --no-cache wget

# Copy built app to Nginx directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create necessary directories and set permissions for OpenShift
# OpenShift assigns arbitrary UIDs, so we need permissive permissions
RUN mkdir -p /tmp/nginx /var/cache/nginx /var/log/nginx && \
    chmod -R 777 /tmp/nginx /var/cache/nginx /var/log/nginx && \
    chmod -R 755 /usr/share/nginx/html

# Remove default Nginx site configs
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/default.d/*

# Expose non-privileged port for OpenShift
EXPOSE 8088

# Healthcheck for OpenShift/Kubernetes
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8088/health || exit 1

# Start Nginx explicitly - this is crucial for OpenShift
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
