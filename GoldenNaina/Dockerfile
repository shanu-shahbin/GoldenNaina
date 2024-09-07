# Start from the official Python base image
FROM python:3.12.1-bullseye

# Set environment variables
ENV PYTHONBUFFERED=1
ENV PORT 8080

# Set the working directory inside the container
WORKDIR /app

# Copy the content of your project into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn GoldenNaina.wsgi:application --bind 0.0.0.0:"${PORT}"

# Expose the application's port
EXPOSE ${PORT}


