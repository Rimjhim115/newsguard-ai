# backend/Dockerfile
# PURPOSE: Build a container for the FastAPI backend.
#
# Each line is a layer — Docker caches layers.
# We copy requirements.txt BEFORE the source code
# so Docker only reinstalls packages when requirements change,
# not on every code change. This makes builds much faster.

# Start from official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies MySQL needs
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the application
# 0.0.0.0 makes it accessible outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]