# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install fastmcp sparqlwrapper

# Expose the port the app runs on
EXPOSE 8898

# Run main.py when the container launches
CMD ["python", "main.py"]

