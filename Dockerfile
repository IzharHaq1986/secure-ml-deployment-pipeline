# Use a slim Python base image to keep the runtime small.
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user for safer container execution.
RUN useradd --create-home --shell /usr/sbin/nologin appuser

# Set the working directory inside the container.
WORKDIR /app

# Copy dependency file first to improve build caching.
COPY requirements.txt .

# Install only the required Python dependencies without cache.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application source code.
COPY app ./app

# Use the non-root user for runtime security.
USER appuser

# Expose the application port.
EXPOSE 8000

# Start the FastAPI service with Uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
