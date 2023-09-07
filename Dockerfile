FROM python:3.9-slim-bookworm as base

RUN apt-get update \
    && apt-get upgrade \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM node:18-bookworm-slim as client-builder

COPY client/package.json client/package-lock.json /app/client/
WORKDIR /app/client

RUN npm install

COPY client /app/client
RUN npm run build

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.6.1

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry config installer.max-workers 10 && \
    poetry config virtualenvs.in-project true
RUN poetry install --only=main --no-root

COPY mmdx ./mmdx
RUN poetry build

# FIXME move this to base stage, along with the activation from final stage
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install dist/mmdx-*.whl


FROM base as final

COPY --from=builder /app/.venv ./.venv
COPY --from=client-builder /app/client/dist/ /app/client/dist/
COPY client/public/ /app/client/public/

# Activate venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Download and cache the model inside the image
RUN <<EOF
python <<HEREDOC
from mmdx.model import ClipModel
model = ClipModel()
HEREDOC
EOF

# Run the application:
# FIXME: use UWSGI server
COPY server.py .
CMD ["python", "server.py"]
