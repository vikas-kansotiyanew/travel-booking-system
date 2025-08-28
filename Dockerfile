FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create staticfiles directory and collect static files
RUN mkdir -p staticfiles && python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application with data population
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py createsu && python manage.py populate_data && python manage.py runserver 0.0.0.0:8000"]