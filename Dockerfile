# DataTrace Dockerfile
# Multi-stage build for production and development

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY poetry.lock pyproject.toml /app/

# Install dependencies with poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

# Production stage
FROM python:3.11-slim as production

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . /app

# Install only runtime dependencies (already installed in builder)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r <(poetry export --without-hashes --format=requirements.txt)

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN useradd --create-home --shell /bin/bash datatrace

# Change ownership of app directory
RUN chown -R datatrace:datatrace /app

# Switch to non-root user
USER datatrace

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2).raise_for_status()" || exit 1

# Run the application
CMD ["python", "-m", "datatrace.server", "--host", "0.0.0.0", "--port", "8000"]
