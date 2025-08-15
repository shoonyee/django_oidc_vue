# Multi-stage build for production deployment in OpenShift
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -r django && \
    useradd -r -g django django

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PORT=8080

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create application directory
WORKDIR /app

# Copy the application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/static /app/media /app/logs && \
    chown -R django:django /app && \
    chmod +x /app/manage.py

# Collect static files
RUN python manage.py collectstatic --noinput --settings=backend.settings

# Switch to non-root user
USER django

# Expose port for the application
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/public/health_check/ || exit 1

# Start the application with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "backend.wsgi:application"]