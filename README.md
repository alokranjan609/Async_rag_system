# Async RAG System

A lightweight asynchronous RAG-style backend built with FastAPI, RQ, and Qdrant.

This project exposes a simple chatbot API that accepts user queries, enqueues them for background processing, and allows clients to poll for job results.

## Project Structure

- `main.py` - Application entrypoint that starts Uvicorn and serves `server.app`.
- `server.py` - FastAPI app with endpoints for health check, enqueuing chat jobs, and checking job status.
- `client/rq_client.py` - RQ queue configuration pointing at Redis-compatible backend on `localhost:6379`.
- `queues/worker.py` - Worker logic for processing queries using HuggingFace and Qdrant.
- `requirements.txt` - Python dependencies for the project.
- `docker-compose.yml` - Local services for Redis-compatible queue backend and Qdrant vector DB.
- `.env` - Environment variable template for HuggingFace and Qdrant settings.
- `.gitignore` - Ignored files for Python, virtual envs, and editor artifacts.

## Prerequisites

- Python 3.11+ (or compatible Python 3.x)
- `pip` installed
- Docker and Docker Compose, if using the included service stack
- A HuggingFace API token for `HUGGINGFACEHUB_API_TOKEN`

## Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy or update the `.env` file with your own values:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
HUGGINGFACE_REPO_ID=deepseek-ai/DeepSeek-V4-Pro
HF_EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=pdf_chunks
```

> Note: The current worker code in `queues/worker.py` sets `HUGGINGFACEHUB_API_TOKEN` directly via `os.environ`. To enable `.env` loading automatically, add `python-dotenv` support and load variables at runtime.

## Running the Service

### Start Docker services

The included `docker-compose.yml` starts the following services:

- `valkey` on `6379` (queue backend)
- `vector-db` on `6333` (Qdrant)

```bash
docker-compose up -d
```

### Start the FastAPI app

```bash
python main.py
```

The app will be available at:

- `http://localhost:8000`

## API Endpoints

### Health Check

```http
GET /
```

Returns:

```json
{"Status": "Server is running!"}
```

### Enqueue a Chat Query

```http
POST /chat?query=your+question+here
```

Returns a job ID and queue status:

```json
{
  "job_id": "<job id>",
  "status": "Query has been enqueued for processing."
}
```

### Get Job Status

```http
GET /job-status?job_id=<job_id>
```

Returns the result once the background worker has completed processing:

```json
{
  "job_id": "<job id>",
  "result": "..."
}
```

## Worker Behavior

The function `process_query` in `queues/worker.py`:

- connects to HuggingFace using `HuggingFaceEndpoint` and `ChatHuggingFace`
- creates embeddings with `HuggingFaceEmbeddings`
- searches a Qdrant vector store for similar documents
- formats a prompt and invokes the model

## Notes

- The app uses RQ for background job processing.
- The queue connection is configured in `client/rq_client.py`.
- If you want the worker to process jobs, run a worker process in a separate terminal such as:

```bash
rq worker
```

(Ensure `RQ` is installed and the queue connection is available.)

## Recommended Improvements

- Load `.env` variables with `python-dotenv` rather than hardcoding the token in code.
- Add a proper worker startup script or process manager.
- Add error handling for missing or unavailable backend services.
- Add a document ingestion step for RAG data indexing.

## License

This repository currently does not specify a license. Add a `LICENSE` file if you want to define usage terms.
