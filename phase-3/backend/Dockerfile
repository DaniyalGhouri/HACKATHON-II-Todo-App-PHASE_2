# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for psycopg2 and other tools
RUN apt-get update && apt-get install -y 
    build-essential 
    libpq-dev 
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
# Note: We copy the 'src', 'api', and other folders
COPY . .

# Expose the port FastAPI will run on
EXPOSE 7860

# Command to run the application
# We use the shim we created earlier (src.main) or point directly to api.index
CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "7860"]
