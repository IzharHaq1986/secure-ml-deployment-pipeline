# Base image:
# Python slim is used to keep the image smaller while remaining practical
# for application runtime and dependency installation.
FROM python:3.12-slim

# Python runtime settings:
# - disable .pyc generation
# - force unbuffered logs for clearer container output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application working directory inside the container
WORKDIR /app

# Install Python dependencies first to improve Docker layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code into the image
COPY . .

# Document the service port used by the FastAPI application
EXPOSE 8000

# Start the FastAPI service with uvicorn
# The module path below assumes the existing repository structure:
# app/main.py containing: app = FastAPI()
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
