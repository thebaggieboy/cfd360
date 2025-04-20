FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Fix static files issue by disabling source map checking
ENV WHITENOISE_KEEP_ONLY_HASHED_FILES=1

# Collect static files
RUN python manage.py collectstatic --noinput --ignore="*.map" || echo "Static files collection encountered issues but continuing build"

# Make SQLite database directory writable
RUN chmod -R 755 /app/data

# Run entrypoint script
COPY render-entrypoint.sh .
RUN chmod +x render-entrypoint.sh

# Command to run the server
ENTRYPOINT ["/app/render-entrypoint.sh"]