# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
