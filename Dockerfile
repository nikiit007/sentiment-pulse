FROM python:3.12-slim

# install curl for the installer
RUN apt-get update && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

# uv installer writes to /root/.local/bin
ENV PATH="/root/.local/bin:${PATH}"
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

# use lockfile for deterministic installs and better caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# app code
COPY dashapp ./dashapp
COPY data ./data

EXPOSE 8050
CMD ["uv", "run", "python", "dashapp/app.py"]
