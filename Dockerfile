FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Detect architecture and download correct uv binary
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        UV_URL="https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz"; \
    elif [ "$ARCH" = "aarch64" ]; then \
        UV_URL="https://github.com/astral-sh/uv/releases/latest/download/uv-aarch64-unknown-linux-gnu.tar.gz"; \
    elif [ "$ARCH" = "armv7l" ]; then \
        UV_URL="https://github.com/astral-sh/uv/releases/latest/download/uv-armv7-unknown-linux-gnueabihf.tar.gz"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    curl -L "$UV_URL" -o uv.tar.gz && \
    tar -xzf uv.tar.gz && \
    mv uv-*/uv /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uv && \
    rm -rf uv.tar.gz uv-*/

WORKDIR /app

COPY . .

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
