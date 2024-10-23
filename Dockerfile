FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    ca-certificates \
    gcc \
    musl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libc-dev \
    libpq-dev \
    file \
    libstdc++6 \
    libx11-6 \
    libxrender1 \
    libxext6 \
    libssl1.1 \
    fontconfig \
    freetype2-demos \
    fonts-droid-fallback \
    fonts-freefont-ttf \
    fonts-liberation \
    build-essential \
    openssl \
    g++ \
    vim \
    && rm -rf /var/lib/apt/lists/*


RUN adduser --disabled-password --gecos "" snappybackend \
    && mkdir /snappybackend \
    && chown -R snappybackend:snappybackend /snappybackend/

USER snappybackend
ENV HOME /home/snappybackend
ENV PATH "$PATH:/home/snappybackend/.local/bin"

WORKDIR /snappybackend

# Copy requirements and install dependencies
COPY requirements.txt /snappybackend/
RUN pip install config
RUN pip install --no-cache-dir -r /snappybackend/requirements.txt

# Copy the rest of the application
COPY ./ /snappybackend/

# Command to run the Django application
# CMD ["sh", "-c", "python manage.py wait_for_db && python manage.py migrate && python manage.py collectstatic -i admin -i rest_framework -i drf-yasg --noinput && python manage.py runserver 0.0.0.0:8000"]
