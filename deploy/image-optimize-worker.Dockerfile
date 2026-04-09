FROM ghcr.io/astral-sh/uv:alpine3.23 AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

RUN apk update --no-cache && apk add --no-cache gcc musl-dev

RUN uv python install 3.13

WORKDIR /app
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --no-editable --locked --only-group image-optimize-worker


FROM alpine:3.23

WORKDIR /app

COPY --from=builder /python /python
COPY --from=builder /app /app
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "faststream", "run", "app.run.image_optimize_worker.app:app"]
