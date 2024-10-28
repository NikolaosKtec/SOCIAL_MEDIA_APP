# Dockerfile

# Base image com Python 3.8
FROM python:3.8


# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory files (on your machine) to the container
ADD . /app/

# install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt




# Expose the port server is running on
EXPOSE 8000

# Start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]