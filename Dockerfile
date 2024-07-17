FROM python:3.9-slim

ARG APP_HOME=/usr/src/app

ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-gdal \
    python3-pip \
    binutils libproj-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock $APP_HOME/

RUN pipenv install --deploy --system --ignore-pipfile

COPY . $APP_HOME/

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
