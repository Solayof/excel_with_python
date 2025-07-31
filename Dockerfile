FROM python:3.12-slim

# Set working directory
WORKDIR .

# Copy only the requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8080

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "CHS_IGBOPE_PORTAL.py", "--server.headless", "true", "--server.port", "8080", "--server.enableCORS", "false"]