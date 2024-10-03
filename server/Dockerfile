# Use an official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Ignore pip error warnings
ENV PIP_ROOT_USER_ACTION=ignore

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Start Flask API and Celery worker
CMD ["sh", "-c", "celery -A tasks worker --loglevel=info -P eventlet & python3 server.py"]