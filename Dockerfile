# Use the official Python image from the Docker Hub
FROM python:3.12.4-slim-bookworm
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .
# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . .
# Check if the DEBUG mode is set to True
RUN sed -i 's/DEBUG = True/DEBUG = False/' /app/UniBoard/settings.py
# Remove any existing migration files and the media directory
RUN rm -r /app/api/migrations/*
RUN rm -r /app/media
# Set environment variables
ENV PYTHONUNBUFFERED=1
# Install supervisord
RUN apt-get update && apt-get install -y supervisor
# Copy the supervisord configuration file into the container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh
EXPOSE 8000
# Run the entrypoint script when the container starts
ENTRYPOINT ["/entrypoint.sh"]
# Command to run the application and celery
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
