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
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked --no-dev --no-install-project

COPY --chown=wagtail:wagtail . .

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
	DJANGO_SETTINGS_MODULE=melita.settings

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

EXPOSE 8000
USER wagtail

CMD set -xe; python manage.py migrate --noinput; gunicorn melita.wsgi:application