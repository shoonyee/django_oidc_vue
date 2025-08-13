# Multi-stage build for Vue.js frontend optimized for OpenShift
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Create non-root user for OpenShift security
RUN addgroup -g 1001 -S appgroup && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G appgroup -g appgroup appuser

# Copy built application from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create necessary directories and set permissions
RUN mkdir -p /tmp/nginx /var/cache/nginx && \
    chown -R appuser:appgroup /usr/share/nginx/html /tmp/nginx /var/cache/nginx && \
    chmod -R 755 /usr/share/nginx/html /tmp/nginx /var/cache/nginx

# Remove default nginx configurations
RUN rm -rf /etc/nginx/conf.d/* /etc/nginx/default.d/*

# Switch to non-root user
USER appuser

# Expose port for OpenShift
EXPOSE 8088

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8088/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
