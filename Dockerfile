FROM python:3.9.16-alpine

ENV PYTHONUNBUFFERED=1

RUN apk --no-cache add \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev libc-dev \
    postgresql-dev \
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
    build-base \
    openssl-dev \
    g++ \
    vim


RUN adduser -D snappybackend \
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
CMD ["python", "manage.py", "runserver", "0.0.0.0:8300"]
