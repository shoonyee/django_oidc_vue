# Single-stage Dockerfile for Vue.js frontend
FROM node:18-alpine

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

# Create nginx directories and set permissions
RUN mkdir -p /var/log/nginx /var/cache/nginx /tmp/nginx

# Expose port 8088 for OpenShift
EXPOSE 8088

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
