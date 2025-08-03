FROM python:3.11-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies for building packages like pandas
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libffi-dev \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        libjpeg-dev \
        zlib1g-dev \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        build-essential \
        curl \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose Streamlit port
EXPOSE 8080

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "CHS_IGBOPE_PORTAL.py", "--server.headless", "true", "--server.port", "8080", "--server.enableCORS", "false"]