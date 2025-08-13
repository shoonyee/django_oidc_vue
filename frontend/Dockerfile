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

# Create a non-root user for OpenShift compatibility (use different group name)
RUN addgroup -g 1001 -S appgroup && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G appgroup -g appgroup nginx

# Copy built app to nginx directory
RUN cp -r dist/* /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create necessary directories with proper permissions for non-root user
RUN mkdir -p /var/cache/nginx /var/log/nginx /tmp/nginx && \
    chown -R nginx:appgroup /var/cache/nginx /var/log/nginx /tmp/nginx /usr/share/nginx/html && \
    chmod -R 755 /var/cache/nginx /var/log/nginx /tmp/nginx /usr/share/nginx/html

# Switch to non-root user
USER nginx

# Expose port 8088 for OpenShift
EXPOSE 8088

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
