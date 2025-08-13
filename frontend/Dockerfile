# Single-stage Dockerfile for Vue.js frontend
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

# Copy built app to nginx directory
RUN cp -r dist/* /var/www/localhost/htdocs/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create nginx user and group
RUN addgroup -g 1001 -S nginx && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx

# Create nginx directories with proper permissions
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/lib/nginx/tmp /tmp/nginx && \
    chown -R nginx:nginx /var/log/nginx /var/cache/nginx /var/lib/nginx /tmp/nginx /var/www/localhost/htdocs && \
    chmod -R 755 /var/log/nginx /var/cache/nginx /var/lib/nginx /tmp/nginx /var/www/localhost/htdocs

# Create writable directories for nginx
RUN mkdir -p /var/lib/nginx/logs /var/lib/nginx/tmp/client_body /var/lib/nginx/tmp/proxy /var/lib/nginx/tmp/fastcgi /var/lib/nginx/tmp/uwsgi /var/lib/nginx/tmp/scgi && \
    chown -R nginx:nginx /var/lib/nginx && \
    chmod -R 755 /var/lib/nginx

# Expose port 8088 for OpenShift
EXPOSE 8088

# Switch to nginx user
USER nginx

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
