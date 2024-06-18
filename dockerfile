# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV FLASK_APP index.py
ENV FLASK_DEBUG true
ENV FLASK_ENV development

# Run index.py when the container launches
CMD ["gunicorn", "index:app", "--bind", "0.0.0.0:8000"]
