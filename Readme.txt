Finance Microservice

Overview

This project implements a microservice for basic financial calculations via a REST API, built with FastAPI and Pydantic. It supports the following endpoints:

POST /finance/loan: Calculates the periodic loan payment and total paid.

POST /finance/compound-interest: Computes compounded future value.

POST /finance/npv: Calculates Net Present Value of a series of cash flows.

POST /finance/irr: Computes Internal Rate of Return for cash flows.

GET /health: Healthcheck endpoint.

All requests are persisted in a SQLite database using SQLAlchemy, and the database schema is created automatically on startup. Swagger UI is available at /docs and OpenAPI spec at /openapi.json.

Technologies

FastAPI for the web framework and automatic docs

Pydantic for request/response models

SQLAlchemy with SQLite for persistence

Uvicorn as ASGI server

Prometheus and Grafana for monitoring

Docker (optional) for containerization

Getting Started

Install dependencies

python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate
pip install -r requirements.txt

Run locally

uvicorn main:application --reload

Test endpoints

Loan:

curl -X POST http://127.0.0.1:8000/finance/loan \
  -H "Content-Type: application/json" \
  -d '{"principal":1000,"annual_rate":5,"years":1,"payments_per_year":12}'

Compound interest:

curl -X POST http://127.0.0.1:8000/finance/compound-interest \
  -H "Content-Type: application/json" \
  -d '{"principal":1000,"annual_rate":5,"periods_per_year":4,"years":3}'

NPV / IRR:

curl -X POST http://127.0.0.1:8000/finance/npv \
  -H "Content-Type: application/json" \
  -d '{"rate":0.05,"cash_flows":[-1000,200,300,400,500]}'

curl -X POST http://127.0.0.1:8000/finance/irr \
  -H "Content-Type: application/json" \
  -d '{"cash_flows":[-1000,200,300,400,500]}'

Monitoring

Start Prometheus with prometheus.yml pointing at http://host.docker.internal:8000/metrics.

Launch Grafana, add Prometheus data source, and build dashboards for http_requests_total metrics.

Docker (optional)

docker build -t finance-api .
docker run -d --name finance-api -p 8000:8000 finance-api:latest

Encountered Issues & Resolutions

Unhashable type: 'list'

When caching functions with @lru_cache, Python raised TypeError: unhashable type: 'list'.

Fix: Removed caching on endpoints that accept list payloads, or converted lists to tuples before caching.

Swagger docs not showing custom routes

Initially omitted including the router into the FastAPI app.

Fix: Added application.include_router(finance_router).

Docker port binding errors

Container failed to start because port 8000 was already in use or previous container name in conflict.

Fix: Removed existing container (docker rm finance-api) before running a new one, or changed container name.

Missing Redis import error

After experimenting with caching libraries, fastapi_redis_cache import remained in main.py, causing ModuleNotFoundError.

Fix: Removed all Redis/cache-specific code since Redis was not used.

Prometheus scraping target down

Prometheus could not reach host.docker.internal:8000 on Windows due to networking config.

Fix: Used localhost:8000 when running service locally, or updated target to the correct host interface in prometheus.yml.

Grafana panels empty

Queries in Grafana returned no data because panels were configured before any requests were issued.

Fix: Made sample API calls, then refreshed dashboards; data appeared correctly.