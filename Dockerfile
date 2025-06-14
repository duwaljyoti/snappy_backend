# ====================
# Stage 1: Build Layer
# ====================
FROM python:3.9.16-alpine AS builder

ENV PYTHONUNBUFFERED=1

# Install system dependencies required to build Python packages
RUN apk --no-cache add \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev libc-dev \
    postgresql-dev \
    build-base \
    openssl-dev \
    g++ \
    libmagic

# Create user and app directory
RUN adduser -D snappybackend \
    && mkdir /snappybackend \
    && chown -R snappybackend:snappybackend /snappybackend/

USER snappybackend
WORKDIR /snappybackend

# Copy only requirements and install dependencies
COPY --chown=snappybackend requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy source code
COPY --chown=snappybackend . .

# =========================
# Stage 2: Runtime Layer
# =========================
FROM python:3.9.16-alpine

ENV PYTHONUNBUFFERED=1

# Install only runtime libraries
RUN apk --no-cache add \
    libffi \
    jpeg \
    zlib \
    libmagic \
    libstdc++ \
    libx11 \
    libxrender \
    libxext \
    libssl1.1 \
    ca-certificates \
    fontconfig \
    freetype \
    ttf-droid \
    ttf-freefont \
    ttf-liberation \
    libpq  # Needed for psycopg2 binary runtime

# Create user and app directory
RUN adduser -D snappybackend \
    && mkdir /snappybackend \
    && chown -R snappybackend:snappybackend /snappybackend/

USER snappybackend
ENV HOME /home/snappybackend
ENV PATH "$PATH:/home/snappybackend/.local/bin"

WORKDIR /snappybackend

# Copy from builder
COPY --from=builder /home/snappybackend/.local /home/snappybackend/.local
COPY --from=builder /snappybackend /snappybackend

# Final run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8300"]
