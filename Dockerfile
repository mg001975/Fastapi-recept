# FROM python:3.11-slim


# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# # Change the working directory to the `app` directory
# WORKDIR /app

# # Install pip and uv system-wide
# # Install dependencies
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --locked --no-install-project

# COPY . .

# RUN uv sync --frozen

# EXPOSE 8000

# CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Install uv




# FROM python:3.12-slim AS builder
# COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/

# # Copy the project into the intermediate image
# ADD . /app

# # Change the working directory to the `app` directory
# WORKDIR /app

# # Install dependencies
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --locked --no-install-project --no-editable



# # Sync the project
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync --locked --no-editable

# FROM python:3.12-slim

# # Copy the environment, but not the source code
# COPY --from=builder --chown=app:app /app/.venv /app/.venv

# EXPOSE 8000
# # Run the application
# CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.12-slim AS builder
# COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/

COPY --from=ghcr.io/astral-sh/uv:0.6.6 /usr/local/bin/uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /usr/local/bin/uvx /usr/local/bin/uvx

# Copy the project into the intermediate image
ADD . /app

# Change the working directory to the `app` directory
WORKDIR /app

RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
