FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .

# Create cache directory
RUN mkdir -p cache

# Expose port
EXPOSE 8001

# Run the application
CMD ["python", "main.py"]
