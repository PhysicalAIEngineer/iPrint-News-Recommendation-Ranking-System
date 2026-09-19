from __future__ import annotations

import os
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from fastapi.responses import Response
from pydantic import BaseModel, Field

APP_NAME = "iPrint News Recommendation & Ranking API"
MODEL_VERSION = os.getenv("MODEL_VERSION", "baseline-v1")
ARTIFACT_ROOT = Path(os.getenv("ARTIFACT_ROOT", "artifacts"))

REQUEST_COUNT = Counter("ip_request_count", "HTTP request count", ["endpoint", "method", "status"])
REQUEST_LATENCY = Histogram("ip_request_latency_seconds", "HTTP request latency", ["endpoint"])
RECOMMENDATION_COUNT = Counter("ip_recommendation_count", "Recommendations returned", ["model"])

app = FastAPI(title=APP_NAME, version="1.0.0")


class RecommendationRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    top_k: int = Field(default=10, ge=1, le=100)
    category: str | None = None


class RecommendationItem(BaseModel):
    article_id: str
    title: str
    score: float
    model_version: str


class RecommendationResponse(BaseModel):
    user_id: str
    model_version: str
    recommendations: list[RecommendationItem]


@app.middleware("http")
async def metrics_middleware(request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - started
    REQUEST_COUNT.labels(request.url.path, request.method, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(elapsed)
    response.headers["X-Model-Version"] = MODEL_VERSION
    return response


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "service": APP_NAME, "model_version": MODEL_VERSION}


@app.get("/model")
def model_info() -> dict:
    return {
        "model_name": "news-ranking-model",
        "model_version": MODEL_VERSION,
        "artifact_root": str(ARTIFACT_ROOT),
    }


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest) -> RecommendationResponse:
    # Production hook: replace this deterministic fallback with the existing
    # candidate-generation + learning-to-rank pipeline from the notebooks.
    candidates = []
    for i in range(request.top_k):
        score = round(1.0 / (i + 1), 6)
        category = request.category or "general"
        candidates.append(
            RecommendationItem(
                article_id=f"{category}-{1000 + i}",
                title=f"{category.title()} news recommendation {i + 1}",
                score=score,
                model_version=MODEL_VERSION,
            )
        )
    RECOMMENDATION_COUNT.labels(MODEL_VERSION).inc(len(candidates))
    return RecommendationResponse(
        user_id=request.user_id,
        model_version=MODEL_VERSION,
        recommendations=candidates,
    )


@app.post("/rank", response_model=list[RecommendationItem])
def rank(items: list[RecommendationItem]) -> list[RecommendationItem]:
    if not items:
        raise HTTPException(status_code=400, detail="items must not be empty")
    return sorted(items, key=lambda x: x.score, reverse=True)


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
