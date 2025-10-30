# Topic Trend & Sentiment Pulse (Local Demo)

This is a local-only sample UI for "Topic Trend & Sentiment Pulse" with MOCK data.

## How to Run

There are two ways to run this project: locally with `uv` or using Docker.

### Local Development (with `uv`)

1.  **Install `uv`**:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Create a virtual environment**:

    ```bash
    uv venv
    ```

3.  **Install dependencies**:

    ```bash
    uv pip install -r requirements.txt
    ```

4.  **Run the application**:

    ```bash
    uv run python dashapp/app.py
    ```

5.  **Open in your browser**:

    Navigate to [http://127.0.0.1:8050](http://127.0.0.1:8050)

### Running with Docker

1.  **Build the Docker image**:

    ```bash
    docker build -t sentiment-pulse .
    ```

2.  **Run the Docker container**:

    ```bash
    docker run -p 8050:8050 sentiment-pulse
    ```

3.  **Open in your browser**:

    Navigate to [http://127.0.0.1:8050](http://127.0.0.1:8050)