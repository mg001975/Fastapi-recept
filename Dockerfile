FROM python:3.11-slim

ENV UV_SYSTEM_PYTHON=1
WORKDIR /app

# Install pip and uv system-wide
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir uv \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv  # maak uv system-wide beschikbaar

COPY . .

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
