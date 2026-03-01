# HTTP Metadata Inventory Service

A FastAPI service that collects and stores HTTP metadata (headers, cookies, page source) for URLs.

## Quick Start

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Documentation

Swagger UI: `http://localhost:8000/docs`

## Endpoints

### POST /metadata

Create a metadata record for a URL.

```bash
curl -X POST "http://localhost:8000/metadata" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Response (201):**
```json
{
  "message": "Metadata stored",
  "data": {
    "url": "https://example.com",
    "headers": {...},
    "cookies": {...},
    "page_source": "<!DOCTYPE html>...",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### GET /metadata

Retrieve metadata for a URL.

```bash
curl "http://localhost:8000/metadata?url=https://example.com"
```

**Response (200):** Returns metadata if found.

**Response (202):** If not found, returns acknowledgement and triggers background collection.
```json
{
  "message": "Metadata collection initiated"
}
```

## Running Tests

```bash
# Run all tests
docker-compose --profile test run --rm test

# Run only unit tests (fast, no DB required)
docker-compose --profile test-unit run --rm test-unit

# Run only integration tests (requires DB)
docker-compose --profile test-integration run --rm test-integration
```

## Project Structure

```
├── main.py                 # FastAPI app entry point
├── cloudsek/
│   ├── api/routes.py       # API endpoints
│   ├── services/
│   │   ├── fetcher.py      # HTTP fetching logic
│   │   └── metadata_service.py  # Business logic
│   ├── workers/
│   │   └── background_worker.py # Async background tasks
│   ├── db/mongo.py         # MongoDB connection
│   ├── schemas/            # Pydantic models
│   └── config.py           # Settings
├── docker-compose.yaml
└── dockerfile
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| MONGO_URL | mongodb://localhost:27017 | MongoDB connection URL |
| DB_NAME | metadata_db | Database name |
