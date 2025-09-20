# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps (for things like pypdf / transformers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

COPY .env .env

# Expose port (Cloud Run will map it automatically)
ENV PORT=8080

# Start with Gunicorn (Flask WSGI server)
CMD ["gunicorn", "-b", ":8080", "main:app"]
