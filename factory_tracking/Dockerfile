FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/storage


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Environment variables (can be overridden at runtime)
ENV DATABASE_URL=sqlite:////app/storage/db.sqlite3
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@localhost

EXPOSE 8000

CMD ["sh", "/app/docker_entrypoint.sh"]
