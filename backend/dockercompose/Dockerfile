# Development Dockerfile for local Docker Compose usage
FROM python:3.9-slim

# Install system dependencies for development
RUN apt-get update && \
    apt-get install -y gcc curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for development
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV DEBUG=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/logs

# Expose port 8080 for the app
EXPOSE 8080

# Run the Django development server with auto-reload
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
