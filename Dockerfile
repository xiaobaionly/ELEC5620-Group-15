# Use a small official Python image
FROM python:3.13-slim

# Basic Python env flags
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create and switch to app directory
WORKDIR /app

# OS dependencies for Pillow (and general builds)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg62-turbo-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better build cache)
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project
COPY . /app

# Expose Django dev server port
EXPOSE 8000

# Default command (overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
