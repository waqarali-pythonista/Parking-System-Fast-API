# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Accept a build argument for the port
ARG PORT

# Set the environment variable
ENV PORT=${BACKEND_PORT}

# Install the required Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the application port (default for FastAPI with uvicorn is 8000)
EXPOSE ${PORT}

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
