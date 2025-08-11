# Finance Microservice

A simple FastAPI-based microservice exposing financial calculation endpoints, with SQLite persistence and Prometheus/Grafana monitoring.

---

## Table of Contents

1. [Features](#features)
2. [Getting Started](#getting-started)
3. [API Endpoints](#api-endpoints)
4. [Monitoring](#monitoring)
5. [Docker](#docker)
6. [Known Issues & Resolutions](#known-issues--resolutions)

---

## Features

* **Loan payment**
* **Compound interest**
* **Net Present Value (NPV)**
* **Internal Rate of Return (IRR)**
* **SQLite** request logging via SQLAlchemy
* **Prometheus** metrics instrumented by `prometheus-fastapi-instrumentator`
* **Grafana** dashboard for visualizing request metrics

---

## Getting Started

### Clone repository

```bash
git clone <repo-url>
cd finance-microservice
```

### Create & activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the service

```bash
uvicorn main:application --reload --port 8000
```

---

## API Endpoints

All endpoints under `/finance`, plus a `/health` check:

### 1. Health Check

**GET** `/health`

Response:

```json
{ "status": "ok" }
```

### 2. Loan Payment

**POST** `/finance/loan`

Request Body:

```json
{
  "principal": float,
  "annual_rate": float,
  "years": int,
  "payments_per_year": int
}
```

Response:

```json
{
  "payment": float,
  "total": float
}
```

### 3. Compound Interest

**POST** `/finance/compound-interest`

Request Body:

```json
{
  "principal": float,
  "annual_rate": float,
  "periods_per_year": int,
  "years": int
}
```

Response:

```json
{
  "future_value": float
}
```

### 4. Net Present Value (NPV)

**POST** `/finance/npv`

Request Body:

```json
{
  "rate": float,
  "cash_flows": [float, …]
}
```

Response:

```json
{
  "npv": float
}
```

### 5. Internal Rate of Return (IRR)

**POST** `/finance/irr`

Request Body:

```json
{
  "cash_flows": [float, …]
}
```

Response:

```json
{
  "irr": float
}
```

---

## Monitoring

### Prometheus

* **Note:** Prometheus was downloaded from the official website and used as a standalone executable. It has been removed from this repository due to size constraints.
* Download & extract Prometheus.
* Configure `prometheus.yml` to scrape `http://<host>:8000/metrics`.

Run:

```bash
./prometheus --config.file=prometheus.yml
```

### Grafana

* **Note:** Grafana was downloaded from the official website and used as a standalone executable. It has been removed from this repository due to size constraints.
* Download & extract Grafana.
* Start server:

```bash
./bin/grafana-server
```

* In web UI (`http://localhost:3000`), add Prometheus as a data source (`http://localhost:9090`).
* Import a dashboard plotting `http_requests_total` by handler and status.

---

## Docker

### Build image

```bash
docker build -t finance-api:latest .
```

### Run container

```bash
docker stop finance-api || true
docker rm finance-api  || true
docker run -d --name finance-api -p 8000:8000 finance-api:latest
```

### Verify

```bash
curl http://localhost:8000/health
```

---

## Known Issues & Resolutions

| Issue                              | Resolution                                                                    |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| IRR endpoint 500 on list input     | Removed `@lru_cache` from IRR & NPV to avoid caching on unhashable list args. |
| Swagger not showing `/finance`     | Added `router.prefix="/finance"` in `main.py`.                                |
| Docker build missing Redis module  | Reverted Redis caching experiments; removed `fastapi_redis_cache` imports.    |
| Prometheus scrape “down” in Docker | Tested scraping locally, ensured metrics endpoint exposed outside container.  |
| Grafana query 502 errors           | Configured Grafana data source URL correctly (`http://localhost:9090`).       |
| PowerShell curl syntax             | Used `Invoke-RestMethod` for Windows HTTP testing.                            |
