# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user first
RUN adduser --disabled-password --gecos "" appuser

# Create log directory and set permissions
RUN mkdir -p /var/log/app && \
    chown -R appuser:appuser /var/log/app

# Upgrade pip and install the required packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set ownership of the application directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    WORKERS=4 \
    LOG_LEVEL=INFO \
    HOST=0.0.0.0 \
    PORT=5000 \
    ALLOWED_EXTENSIONS=csv \
    MAX_CONTENT_LENGTH=16777216 \
    UPLOAD_FOLDER=/tmp \
    DATE_FORMAT="%d %b %Y" \
    NUMERIC_COLUMNS="Paid out,Paid in,Balance" \
    SKIP_ROWS=3 \
    DEBUG=False

# Run Gunicorn with proper settings and logging
CMD ["sh", "-c", "gunicorn --bind $HOST:$PORT --workers $WORKERS --timeout 120 \
     --access-logfile /var/log/app/access.log \
     --error-logfile /var/log/app/error.log \
     --log-level $LOG_LEVEL \
     --capture-output \
     app:app"]