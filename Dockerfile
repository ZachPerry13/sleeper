# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to indicate the app is running in production mode
ENV FLASK_ENV=production

# Define App
ENV FLASK_APP=app.py

# Run the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]