# Stage 1: Build stage
FROM python:3.11.6-slim as builder

# Set up virtual environment to install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install dependencies in the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.11.6-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set a writable directory for Matplotlib configuration
ENV MPLCONFIGDIR=/tmp/matplotlib_cache

WORKDIR /app

# Copy the Python scripts
COPY --chown=appuser:appuser perf.py .

# Command to run the script, URL must be provided as an argument
ENTRYPOINT ["python", "perf.py"]
