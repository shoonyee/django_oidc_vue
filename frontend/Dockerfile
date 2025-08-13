# Single-stage Dockerfile for Vue.js frontend optimized for OpenShift
FROM node:20-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Install nginx
RUN apk add --no-cache nginx

# Create a non-root user for OpenShift compatibility 
RUN addgroup -g 1001 -S appgroup && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G appgroup -g appgroup appuser

# Create nginx html directory and copy built app
RUN mkdir -p /usr/share/nginx/html && \
    cp -r dist/* /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create all necessary directories with proper permissions for non-root user
RUN mkdir -p /var/cache/nginx /var/log/nginx /tmp/nginx /tmp/nginx/client_body /tmp/nginx/proxy /tmp/nginx/fastcgi /tmp/nginx/uwsgi /tmp/nginx/scgi && \
    chown -R appuser:appgroup /var/cache/nginx /var/log/nginx /tmp/nginx /usr/share/nginx/html && \
    chmod -R 755 /var/cache/nginx /var/log/nginx /tmp/nginx /usr/share/nginx/html

# Remove default nginx configuration that might cause permission issues
RUN rm -f /etc/nginx/conf.d/default.conf

# Switch to non-root user
USER appuser

# Expose port 8088 for OpenShift
EXPOSE 8088

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
