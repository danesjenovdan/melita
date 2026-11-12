# ---------------------------------- WARNING ----------------------------------
# This file is primarily for production use with k8s
# See Dockerfile in subdirectories for dev use with docker-compose
# ---------------------------------- WARNING ----------------------------------

# ---
# build scss in separate image
# ---
FROM node:25-alpine as sass-compile

WORKDIR /app

COPY ./sass-compile/package.json ./sass-compile/yarn.lock ./
RUN yarn

COPY ./sass-compile/scss ./scss

RUN yarn css


FROM python:3.14-slim AS builder

RUN useradd wagtail

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
    libicu-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Install dependencies first (cached separately from app code changes).
COPY melita/pyproject.toml melita/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

COPY --chown=wagtail:wagtail melita/ .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

RUN python3 manage.py compilemessages

FROM python:3.14-slim AS runtime

WORKDIR /app

RUN useradd wagtail

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libicu76 \
    && rm -rf /var/lib/apt/lists/*

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=melita.settings \
    PYTHONUNBUFFERED=1 \
    PORT=8000


COPY --chown=wagtail:wagtail --from=builder /opt/venv /opt/venv
COPY --chown=wagtail:wagtail --from=builder /app /app

# Copy compiled css from other image
COPY --chown=wagtail:wagtail --from=sass-compile /app/static/css ./melita/static/css

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

EXPOSE 8000

CMD gunicorn melita.wsgi:application -b 0.0.0.0:8000 --log-level DEBUG --no-control-socket