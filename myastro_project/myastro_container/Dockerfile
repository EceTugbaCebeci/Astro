# Use the official Python image from the Docker Hub
FROM python:3.12.3

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . /code/

# Expose the port your app runs on
EXPOSE 8000

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=myastro.settings
ENV PYTHONUNBUFFERED=1

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
