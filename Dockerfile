# Base Image
FROM python:3.11-slim

# WorkDir
WORKDIR /app

# System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create data folder
RUN mkdir -p data

# Expose port
EXPOSE 8000

# start command
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]