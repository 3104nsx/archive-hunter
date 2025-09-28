
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Amsterdam

# Create app user (optional enhancement later to run non-root)
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy only the whitelisted repo content (compose bind-mounts data dirs)
COPY . /app

# Create runtime dirs
RUN mkdir -p /app/data/logs /app/data/cache /app/backups /app/exports

# Default command is the dashboard (override per service in compose)
CMD ["python", "tools/dashboard.py"]
