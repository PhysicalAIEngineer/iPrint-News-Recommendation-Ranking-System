# iPrint News Recommendation & Ranking System

> **End-to-end personalized news recommendation, semantic retrieval, candidate generation, and learning-to-rank platform for iPrint.**

[![CI](https://github.com/PhysicalAIEngineer/iPrint-News-Recommendation-Ranking-System/actions/workflows/ci.yml/badge.svg)](https://github.com/PhysicalAIEngineer/iPrint-News-Recommendation-Ranking-System/actions/workflows/ci.yml)
[![Model Validation](https://github.com/PhysicalAIEngineer/iPrint-News-Recommendation-Ranking-System/actions/workflows/model-validation.yml/badge.svg)](https://github.com/PhysicalAIEngineer/iPrint-News-Recommendation-Ranking-System/actions/workflows/model-validation.yml)

---

## 1. Project Overview

iPrint is an upcoming media house in India providing news and information services across domains such as sports, weather, education, health, research, stocks, technology, and other information categories.

Historically, the platform relied heavily on **popular-content and similarity-based recommendations**. This creates two important product problems:

1. A user can repeatedly receive popular or already-familiar stories instead of discovering new interests.
2. A recommendation system based only on previously consumed content can have limited ability to balance **relevance, freshness, diversity, and discovery**.

This project builds a production-oriented recommendation and ranking system that combines:

- user behavior and interaction history,
- article/content features,
- contextual information,
- candidate-generation strategies,
- semantic retrieval,
- learning-to-rank,
- model evaluation,
- experiment tracking,
- API serving,
- caching and persistence,
- monitoring and observability.

The target experience is a personalized news feed that can introduce **new, relevant articles** while respecting article availability and user-history constraints.

---

# 2. Business Problem

iPrint wants to personalize its home-page experience at the start of the day and also recommend related articles after a user reads an article.

### Primary recommendation use cases

### A. Daily personalized Top-10 feed

When a user opens the application, the system should generate:

> **Top 10 relevant and discoverable news articles for that user.**

The recommendation should use signals such as:

- historical reading/click behavior,
- user preferences,
- article/content characteristics,
- recency and freshness,
- contextual information,
- semantic similarity,
- candidate-generation scores,
- learning-to-rank features.

### B. Article-to-article recommendations

When the user clicks article **A**, the system should generate:

> **Top 10 articles related to article A.**

The related-content pipeline can use:

- content similarity,
- semantic embeddings,
- metadata,
- keyword similarity,
- article freshness,
- candidate-generation filters,
- ranking scores.

---

# 3. Recommendation Constraints

The recommendation system must enforce important business constraints.

| Constraint | Requirement |
|---|---|
| Top-K feed | Return top 10 recommendations for the daily feed |
| Similar articles | Return top 10 related articles for a clicked article |
| Removed content | Never recommend unavailable/pulled articles |
| Seen content | Avoid articles already seen by the user |
| Language | Content-based recommendations consider English-language articles |
| Freshness | Incorporate article recency |
| Discovery | Allow relevant new content outside the user's historical consumption |
| Diversity | Avoid returning highly repetitive content |
| Ranking | Final recommendations are ordered by relevance/ranking score |
| Output | Return article title/name and article ID |

---

# 4. High-Level Architecture

The complete production-oriented pipeline is:

```text
Data
  ↓
Feature Engineering
  ↓
Candidate Generation
  ↓
Semantic Retrieval
  ↓
Learning-to-Rank
  ↓
MLflow
  ↓
FastAPI
  ↓
Redis / PostgreSQL
  ↓
Streamlit
  ↓
Prometheus / Grafana
```

### Architecture diagram

The system separates the recommendation lifecycle into five logical layers:

1. **Data & ML pipeline**
2. **Candidate retrieval and ranking**
3. **Model lifecycle**
4. **Production serving and storage**
5. **Dashboard, monitoring, and observability**

---

# 5. End-to-End Recommendation Flow
<img width="1536" height="1024" alt="ChatGPT Image Sep 19, 2026, 06_40_55 PM" src="https://github.com/user-attachments/assets/8b06c519-5521-4293-86a0-256f684250a4" />


# 6. Data

The project uses two principal datasets.

## Consumer transactions

`Dataset/consumer_transanctions.csv`

The transaction dataset contains user interaction signals.

| Feature | Purpose |
|---|---|
| `consumer_id` | User identifier |
| `item_id` | Article identifier |
| `event_timestamp` | Temporal behavior / recency |
| `interaction_type` | Implicit feedback signal |
| `consumer_session_id` | Session-level modeling |
| `consumer_device_info` | Device/context feature |
| `consumer_location` | Contextual personalization |
| `country` | Geographic context |

## Platform content

`Dataset/platform_content.csv`

| Feature | Purpose |
|---|---|
| `item_id` | Article identifier / join key |
| `title` | Text representation |
| `text_description` | Article content representation |
| `language` | Language filtering |
| `item_type` | HTML / VIDEO / RICH content type |
| `producer_id` | Producer affinity |
| `event_timestamp` | Content freshness |
| `interaction_type` | Availability / pulled-content handling |

The complete field definitions are documented in [docs/data_dictionary.md](docs/data_dictionary.md).

---

# 7. Data Processing & Feature Engineering

The feature-engineering layer transforms raw user and content data into recommendation-ready representations.

### User features

Examples include:

- historical interaction counts,
- recency of interaction,
- session activity,
- user-item interaction statistics,
- user embeddings,
- behavioral preferences.

### Article features

Examples include:

- title features,
- description features,
- category/topic information,
- freshness,
- producer information,
- article embeddings,
- language and content-type metadata.

### Context features

Examples include:

- device,
- location,
- country,
- session context,
- time-related features.

### Generated feature artifacts

```text
artifacts/features/
├── article_features.parquet
├── article_embeddings.npy
├── article_embedding_index.parquet
├── producer_features.parquet
├── session_features.parquet
├── user_features.parquet
├── user_embeddings.npy
├── user_embedding_index.parquet
└── user_item_features_raw.parquet
```

---

# 8. Candidate Generation

A recommendation system should not rank every article in the entire catalog for every request.

Instead, the system first creates a smaller candidate set.

The project supports multiple candidate-generation signals:

### 1. Popularity / rule-based candidates

Useful for:

- fresh content,
- globally popular stories,
- category-aware recommendations.

### 2. Collaborative filtering

Uses user-item interaction behavior to identify articles consumed by users with similar preferences.

### 3. Content-based retrieval

Uses article metadata and textual representations to find content related to user interests or a clicked article.

### 4. Hybrid candidate generation

Combines multiple candidate sources before the ranking stage.

Generated artifacts include:

```text
artifacts/candidates/
├── raw_candidates.parquet
├── candidate_features.parquet
├── candidate_features.csv
├── candidate_generation_config.json
└── test_truth.parquet
```

---

# 9. Semantic Retrieval

Semantic retrieval improves recommendation beyond exact keyword matching.

The article title and description can be transformed into dense vector representations.

The project contains:

```text
artifacts/semantic/
├── semantic_candidates.parquet
├── semantic_config.json
└── semantic_recommendations.csv
```

The vector-search layer uses FAISS artifacts:

```text
artifacts/indexes/faiss/
├── article_cosine.index
└── article_metadata.parquet
```

Conceptually:

```text
Article / User Query
       ↓
Text Representation
       ↓
Embedding Model
       ↓
Dense Vector
       ↓
FAISS Similarity Search
       ↓
Relevant Candidate Articles
```

This is particularly useful for the **"articles similar to clicked article A"** use case.

---

# 10. Learning-to-Rank

Candidate generation focuses on **recall**.

Learning-to-rank focuses on the final ordering and **relevance**.

The ranking model receives candidate-level features such as:

```text
User Features
      +
Article Features
      +
Context Features
      +
Candidate Source Features
      +
Semantic Similarity
      +
Freshness
      ↓
Learning-to-Rank Model
      ↓
Ranking Score
      ↓
Top-K Articles
```

The repository contains a LightGBM ranking artifact:

```text
artifacts/ltr/
├── lightgbm_ltr_model.txt
├── ltr_config.json
├── ltr_feature_config.json
├── feature_importance.csv
├── ranking_evaluation.csv
├── validation_predictions.parquet
├── final_meta.parquet
└── example_top10_recommendations.csv
```

---

# 11. Evaluation

The system is designed to evaluate recommendation quality at multiple levels.

## Ranking metrics

### Precision@K

Measures how many of the top-K recommendations are relevant.

```text
Precision@K =
relevant recommendations in top-K
---------------------------------
K
```

### Recall@K

Measures how much of the relevant content was retrieved.

### NDCG@K

Measures ranking quality while giving greater importance to highly ranked relevant items.

### MRR

Measures the position of the first relevant recommendation.

## Product/recommendation metrics

The evaluation contract also includes:

- Coverage
- Diversity
- Novelty
- CTR

These metrics help evaluate the discovery objective rather than relevance alone.

Run the evaluation entry point with:

```bash
python training/evaluate.py
```

The reusable metric implementations are in:

```text
training/metrics.py
```

---

# 12. Recommendation Output



https://github.com/user-attachments/assets/b999907b-edaf-4411-b017-015082c0334c



The final recommendation response should contain the article ID and article title.

Example:

```json
{
  "user_id": "u1",
  "model_version": "baseline-v1",
  "cached": false,
  "recommendations": [
    {
      "article_id": "technology-1001",
      "title": "Technology news recommendation 1",
      "score": 1.0,
      "model_version": "baseline-v1"
    }
  ]
}
```

For a production model integration, the same response contract can be retained while replacing the deterministic serving adapter with the trained candidate-generation and LTR artifacts.

---

# 13. Production Serving Layer

## FastAPI

The API layer is located in:

```text
api/
├── main.py
├── cache.py
├── db.py
├── Dockerfile
└── requirements.txt
```

Available endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| GET | `/ready` | Readiness / database state |
| GET | `/model` | Model metadata |
| POST | `/recommend` | Generate recommendations |
| POST | `/rank` | Rank supplied recommendation items |
| GET | `/metrics` | Prometheus metrics |

### Recommendation request

```json
{
  "user_id": "u1",
  "top_k": 10,
  "category": "technology"
}
```

---

# 14. Redis

Redis provides a low-latency caching layer for recommendation responses.

Conceptually:

```text
User Request
     ↓
FastAPI
     ↓
Redis lookup
     ├── Cache hit → return recommendations
     │
     └── Cache miss
             ↓
       Recommendation pipeline
             ↓
          Redis SET
             ↓
       Return response
```

The cache key includes model/user/category/top-K information so cached recommendations can be associated with the relevant request context.

---

# 15. PostgreSQL

PostgreSQL provides persistent storage for production-oriented application data.

Potential persisted entities include:

- users,
- articles,
- interaction logs,
- metadata,
- recommendation events,
- operational state.

The database readiness check is exposed through:

```text
GET /ready
```

---

# 16. MLflow

MLflow is used for experiment and model lifecycle management.

The project includes:

```text
training/mlflow_train.py
```

The lifecycle is:

```text
Experiment
   ↓
Parameters
   ↓
Training / Evaluation
   ↓
Metrics
   ↓
MLflow Tracking
   ↓
Model Version
   ↓
Serving
```

Run locally:

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
python training/mlflow_train.py
```

The Docker stack exposes MLflow on port **5000**.

---

# 17. Streamlit Recommendation Dashboard

The Streamlit application is located at:

```text
dashboard/app.py
```

The dashboard provides operational views for:

### Overview

- API status
- model version
- recommendation engine state
- observability status
- production architecture

### Live Recommendations

- user ID
- category
- Top-K selection
- recommendation results
- recommendation scores
- latency

### Ranking Analytics

- Precision@K
- Recall@K
- NDCG@K
- MRR
- Coverage
- Diversity
- Novelty

### Model & MLflow

- model version
- experiment
- lifecycle state
- MLflow integration

### Monitoring

- API health
- model state
- Prometheus metrics
- cache statistics
- database readiness

---

# 18. Monitoring & Observability

The API exposes Prometheus-compatible metrics at:

```text
GET /metrics
```

The monitoring stack consists of:

```text
FastAPI
   ↓
Prometheus Metrics
   ↓
Prometheus
   ↓
Grafana
```

Relevant production metrics include:

- HTTP request count
- recommendation request count
- request latency
- recommendation volume
- cache hits
- model-loaded state
- database readiness

Recommended operational dashboards include:

- request throughput,
- P50/P95/P99 latency,
- HTTP error rate,
- recommendation volume,
- cache hit rate,
- model version,
- ranking metrics,
- resource utilization,
- recommendation drift.

---

# 19. Repository Structure

```text
iPrint-News-Recommendation-Ranking-System/
│
├── Dataset/
│   ├── consumer_transanctions.csv
│   └── platform_content.csv
│
├── Notebook/
│   ├── 01_EDA & Data Preparation.ipynb
│   ├── 02_Feature Engineering.ipynb
│   ├── 03_Baseline_Recommenders.ipynb
│   ├── 04_Semantic_Retrieval.ipynb
│   ├── 05_Candidate_Generation.ipynb
│   └── 06_Learning_To_Rank.ipynb
│
├── artifacts/
│   ├── baselines/
│   ├── candidates/
│   ├── eda/
│   ├── features/
│   ├── indexes/
│   ├── ltr/
│   ├── processed/
│   └── semantic/
│
├── api/
│   ├── main.py
│   ├── cache.py
│   ├── db.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── dashboard/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── training/
│   ├── evaluate.py
│   ├── metrics.py
│   └── mlflow_train.py
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│
├── tests/
│   └── test_api.py
│
├── docs/
│   ├── data_dictionary.md
│   └── eda_findings.md
│
├── requirements.txt
├── requirements-api.txt
├── requirements-dashboard.txt
├── docker-compose.yml
└── README.md
```

---

# 20. Notebook / Research Pipeline

The six notebooks represent the main analytical and modeling workflow.

| Notebook | Purpose |
|---|---|
| 01 | EDA and data preparation |
| 02 | Feature engineering |
| 03 | Baseline recommenders |
| 04 | Semantic retrieval |
| 05 | Candidate generation |
| 06 | Learning-to-rank |

Recommended execution order:

```text
01 EDA & Data Preparation
        ↓
02 Feature Engineering
        ↓
03 Baseline Recommenders
        ↓
04 Semantic Retrieval
        ↓
05 Candidate Generation
        ↓
06 Learning To Rank
        ↓
Evaluation
        ↓
Serving
```

---

# 21. Baseline → Hybrid → LTR Evolution

The project is designed as an incremental recommendation architecture.

### Stage 1 — Baseline

Popular and similarity-based approaches establish a reference point.

### Stage 2 — Collaborative filtering

User-item interaction patterns provide personalized candidates.

### Stage 3 — Content-based recommendation

Article metadata and textual representations identify similar content.

### Stage 4 — Semantic retrieval

Dense embeddings and vector search capture semantic relationships beyond exact lexical overlap.

### Stage 5 — Hybrid candidate generation

Multiple candidate sources are combined.

### Stage 6 — Learning-to-rank

Candidate features and semantic/context signals are used to produce the final ranking.

This architecture separates **retrieval** from **ranking**, allowing each stage to be improved independently.

---

# 22. Cold Start & Discovery

A production news recommender needs to address users and articles with limited interaction history.

Potential strategies include:

### New user

Use:

- trending content,
- fresh articles,
- category-level popularity,
- contextual signals,
- onboarding preferences.

### New article

Use:

- article embeddings,
- content metadata,
- freshness,
- producer/category information,
- semantic retrieval.

### Discovery

The ranking layer can combine relevance with discovery-oriented signals such as:

```text
Final Score =
Relevance
+ Semantic Similarity
+ Freshness
+ User Affinity
+ Discovery Signal
- Repetition Penalty
```

The exact production scoring function should be calibrated against offline and online evaluation data.

---

# 23. Online Feedback Loop

The intended production feedback loop is:

```text
Recommendation
      ↓
User Impression
      ↓
Click / No Click
      ↓
Interaction Event
      ↓
Training Dataset
      ↓
Feature Engineering
      ↓
Candidate Generation
      ↓
LTR Retraining
      ↓
Evaluation
      ↓
MLflow
      ↓
New Model Version
      ↓
API Serving
```

This allows the recommendation system to continuously learn from user behavior.

---

# 24. Local Development

## Clone

```bash
git clone https://github.com/PhysicalAIEngineer/iPrint-News-Recommendation-Ranking-System.git
cd iPrint-News-Recommendation-Ranking-System
```

## Install the development environment

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install the complete research environment:

```bash
pip install -r requirements.txt
```

For API-only development:

```bash
pip install -r requirements-api.txt
```

For dashboard-only development:

```bash
pip install -r requirements-dashboard.txt
```

---

# 25. Run FastAPI

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

Health check:

```bash
curl http://localhost:8000/health
```

Recommendation request:

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","top_k":10,"category":"technology"}'
```

---

# 26. Run Streamlit

```bash
streamlit run dashboard/app.py
```

Open:

```text
http://localhost:8501
```

---

# 27. Run the Complete Stack

The repository contains a production-like local Docker Compose environment.

```bash
docker compose up --build
```

Services:

| Service | Port | Purpose |
|---|---:|---|
| FastAPI | 8000 | Recommendation API |
| Streamlit | 8501 | Recommendation dashboard |
| MLflow | 5000 | Experiment tracking |
| PostgreSQL | 5432 | Persistent data |
| Redis | 6379 | Recommendation cache |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Monitoring dashboards |

Stop services:

```bash
docker compose down
```

---

# 28. Testing

Run all tests:

```bash
pytest -q
```

Run linting:

```bash
ruff check api tests training dashboard
```

The CI pipeline validates:

- dependency installation,
- Ruff linting,
- Python compilation,
- API tests,
- Docker builds,
- Docker Compose configuration.

---

# 29. CI/CD

GitHub Actions workflows are located in:

```text
.github/workflows/
├── ci.yml
└── model-validation.yml
```

### CI

Validates application code and infrastructure changes.

### Model Validation

Validates changes related to:

- training,
- model artifacts,
- notebooks,
- evaluation,
- serving,
- dependency configuration.

The goal is to prevent broken recommendation or serving changes from reaching the production deployment path.

---

# 30. Production Model Integration Status

The repository contains real offline artifacts for:

- feature engineering,
- candidate generation,
- semantic retrieval,
- FAISS indexing,
- LightGBM learning-to-rank,
- evaluation outputs.

However, the current FastAPI serving layer intentionally contains a **deterministic fallback adapter** so the API remains runnable without requiring the full research/model artifact environment.

Therefore:

```text
Offline ML Pipeline
      │
      ├── Real artifacts
      │      ├── FAISS
      │      ├── embeddings
      │      └── LightGBM LTR
      │
      └── FastAPI
             │
             └── Current deterministic fallback
```

The next production integration step is to load the serialized candidate-generation, semantic-retrieval, and LTR artifacts into the API recommendation path.

---

# 31. Recommended Production Integration

A production recommendation request should eventually follow:

```text
POST /recommend
      ↓
Validate user
      ↓
Load user profile/history
      ↓
Retrieve eligible articles
      ↓
Remove pulled/unavailable content
      ↓
Remove already-seen articles
      ↓
Generate candidates
      ↓
Semantic retrieval
      ↓
Build ranking features
      ↓
LightGBM LTR
      ↓
Apply freshness/diversity constraints
      ↓
Top 10
      ↓
Redis cache
      ↓
Return article ID + title + score
```

For clicked-article recommendations:

```text
POST /recommend-related
      ↓
Article A
      ↓
Article embedding
      ↓
FAISS nearest-neighbor search
      ↓
English-language filter
      ↓
Availability filter
      ↓
Exclude current article
      ↓
Rank candidates
      ↓
Top 10 related articles
```

---


# 32. Security & Configuration

Production credentials must never be committed to Git.

Use environment variables or a secret manager for:

```text
DATABASE_URL
REDIS_URL
MLFLOW_TRACKING_URI
API credentials
database credentials
cloud credentials
```

The repository's Docker and API configuration is designed so these values can be injected at runtime.

---

# 34. Technology Stack

### Data & ML

- Python
- Pandas
- NumPy
- Scikit-learn
- Implicit
- LightGBM
- Sentence Transformers
- Transformers
- FAISS

### Serving

- FastAPI
- Uvicorn
- Pydantic

### Storage / Cache

- PostgreSQL
- SQLAlchemy
- Redis

### MLOps

- MLflow
- Docker
- Docker Compose
- GitHub Actions

### Dashboard

- Streamlit
- Plotly

### Observability

- Prometheus
- Grafana
- Prometheus Python client

---

# 35. Project Outcome

The resulting architecture transforms iPrint from a simple popularity/similarity recommendation workflow into a modular recommendation platform:

```text
Raw User + Content Data
          ↓
Feature Engineering
          ↓
Multiple Candidate Sources
          ↓
Semantic Retrieval
          ↓
Learning-to-Rank
          ↓
Personalized Top-K
          ↓
FastAPI
          ↓
Redis / PostgreSQL
          ↓
Streamlit
          ↓
Prometheus / Grafana
          ↓
Continuous Feedback
          ↺
```

The design explicitly separates **data preparation, retrieval, ranking, model lifecycle, serving, persistence, dashboarding, and observability**, making the system easier to evaluate, test, deploy, and extend.

---

## License

This project is released under the [MIT License](LICENSE).
