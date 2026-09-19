# iPrint News Recommendation & Ranking System

Production-oriented news recommendation and learning-to-rank platform.

## Architecture

Data -> feature engineering -> candidate generation -> semantic retrieval -> learning-to-rank -> MLflow -> FastAPI -> Redis/PostgreSQL -> Streamlit -> Prometheus/Grafana.

The original notebooks remain the research/model-development layer. The production layer adds serving, experiment tracking, containers, testing, CI, and observability.

## Repository

- Dataset/ - transaction and platform-content data
- Notebook/ - EDA, feature engineering, baseline recommenders, semantic retrieval, candidate generation and learning-to-rank
- artifacts/ - generated model/data artifacts
- api/ - FastAPI serving layer
- training/ - evaluation entry points
- mlflow/ - MLflow integration
- dashboard/ - Streamlit recommendation dashboard
- monitoring/ - Prometheus/Grafana configuration
- tests/ - API tests
- .github/workflows/ - CI and model validation
- docker-compose.yml - local production-like stack

## Run locally

```bash
uvicorn api.main:app --reload
```

Open http://localhost:8000/docs.

Endpoints:
- GET /health
- GET /model
- POST /recommend
- POST /rank
- GET /metrics

Example request:
```json
{
  "user_id": "u1",
  "top_k": 10,
  "category": "technology"
}
```

## Docker

```bash
docker compose up --build
```

| Service | Port |
|---|---:|
| FastAPI | 8000 |
| Streamlit | 8501 |
| MLflow | 5000 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Prometheus | 9090 |
| Grafana | 3000 |

## MLflow

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
python mlflow/train_and_log.py
```

The logging script provides the integration point for metrics emitted by the existing learning-to-rank pipeline.

## Evaluation

The evaluation contract includes Precision@K, Recall@K, NDCG@K, MRR, Coverage, Diversity, Novelty and CTR when interaction feedback is available.

```bash
python training/evaluate.py
```

## Testing

```bash
pytest -q
```

## CI/CD

GitHub Actions validates dependencies, API tests and Docker builds on pushes and pull requests. Model validation runs when training/model code changes.

## Monitoring

FastAPI exposes Prometheus metrics at /metrics. Prometheus scrapes the API and Grafana is configured with Prometheus as its default data source.

Recommended dashboards include request throughput, P50/P95/P99 latency, error rate, recommendation volume, model version, ranking metrics, drift, cache hit rate and resource utilization.

## Production model integration

The API currently contains a deterministic fallback so the service is runnable immediately. The next integration point is to load the serialized artifacts produced by the existing notebooks and connect the real candidate-generation and learning-to-rank pipeline to POST /recommend.

Use environment variables or a secret manager for production credentials. Do not commit secrets.
