# Parent Image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing pyc files to disc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Set the Python path so imports work relative to the WORKDIR
ENV PYTHONPATH /usr/src/app

# Install system dependencies if needed (might be necessary for some Scrapy dependencies)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# No explicit command here, as we'll run commands via docker-compose exec
# CMD ["scrapy", "crawl", "job_spider"] # You could uncomment this to run the spider automatically on container start if desired