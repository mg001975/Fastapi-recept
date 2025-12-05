# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Copy project files
# COPY . /app

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Ensure uvicorn is in requirements.txt
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
FROM python:3.11-slim

ENV UV_SYSTEM_PYTHON=1
WORKDIR /app

RUN pip install --no-cache-dir uv

COPY . .

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
