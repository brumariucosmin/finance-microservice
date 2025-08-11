# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8000"]
