# ====================
# Stage 1: Build Layer
# ====================
FROM python:3.9.16-alpine AS builder

ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apk --no-cache add \
    gcc python3-dev musl-dev postgresql-dev build-base libffi-dev

WORKDIR /app

# Create a virtual environment and install dependencies there
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# =========================
# Stage 2: Runtime Layer
# =========================
FROM python:3.9.16-alpine

ENV PYTHONUNBUFFERED=1
# CRITICAL: This ensures the system finds 'celery' and 'python' in our venv
ENV PATH="/opt/venv/bin:$PATH"

# Runtime dependencies
RUN apk --no-cache add libpq openssl tzdata curl

# Set up the user
RUN adduser -D snappybackend
WORKDIR /home/snappybackend/app

# 1. Copy the virtual environment from the builder
COPY --from=builder /opt/venv /opt/venv

# 2. Copy the app code and ensure the user owns it
COPY --from=builder --chown=snappybackend:snappybackend /app .

USER snappybackend

# Final run command (Overridden by docker-compose for worker/beat)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8300"]
