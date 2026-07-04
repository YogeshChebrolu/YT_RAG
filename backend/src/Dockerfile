FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install ffmpeg and build deps for native packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        build-essential \
        libffi-dev \
        libssl-dev \
        git && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy requirements and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the source code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD [".venv/bin/python", "core/main.py"]