
FROM python:3.9-slim-bullseye


WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Environment variables
ENV PYTHONPATH=/app
ENV JD_PATH=/app/data/job_descriptions/software_engineer_jd.txt

# Run both APIs
CMD ["sh", "-c", "python deployment/api_resume.py & python deployment/api_sentiment.py"]