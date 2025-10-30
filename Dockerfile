# 1. Use slim Python base
FROM python:3.12-slim AS base

# 2. Install uv (tiny binary)
ENV PATH="/root/.cargo/bin:${PATH}"
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app
COPY requirements.txt ./

# 3. Install deps in one layer
RUN uv pip install -r requirements.txt --no-cache

# 4. Copy source code
COPY dashapp ./dashapp
COPY data ./data

# 5. Run app
EXPOSE 8050
CMD ["uv", "run", "python", "dashapp/app.py"]
