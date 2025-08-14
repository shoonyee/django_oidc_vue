# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev curl default-libmysqlclient-dev pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/logs

# Set proper permissions
RUN chmod +x /app/manage.py

# Expose port for the application
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/public/health_check/ || exit 1

# Start the application with all necessary setup commands
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]