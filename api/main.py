from __future__ import annotations
import os, time
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel, Field
from api.cache import get_cached, set_cached
from api.db import db_healthcheck

APP_NAME="iPrint News Recommendation & Ranking API"
MODEL_VERSION=os.getenv("MODEL_VERSION","baseline-v1")
REQUEST_COUNT=Counter("ip_request_count","HTTP requests",["endpoint","method","status"])
REQUEST_LATENCY=Histogram("ip_request_latency_seconds","Request latency",["endpoint"])
RECOMMENDATION_COUNT=Counter("ip_recommendation_count","Recommendation items returned",["model"])
CACHE_HIT_COUNT=Counter("ip_cache_hit_count","Recommendation cache hits")
MODEL_LOADED=Gauge("ip_model_loaded","Whether serving model is loaded"); MODEL_LOADED.set(1)
app=FastAPI(title=APP_NAME,version="1.0.0",default_response_class=ORJSONResponse)

class RecommendationRequest(BaseModel):
    user_id:str=Field(...,min_length=1); top_k:int=Field(10,ge=1,le=100); category:str|None=None
class RecommendationItem(BaseModel):
    article_id:str; title:str; score:float; model_version:str
class RecommendationResponse(BaseModel):
    user_id:str; model_version:str; cached:bool; recommendations:list[RecommendationItem]

def generate_recommendations(request:RecommendationRequest):
    # Adapter point for the existing candidate-generation + learning-to-rank artifacts.
    category=request.category or "general"
    return [RecommendationItem(article_id=f"{category}-{1000+i}",title=f"{category.title()} news recommendation {i+1}",score=round(1/(i+1),6),model_version=MODEL_VERSION) for i in range(request.top_k)]

@app.middleware("http")
async def metrics_middleware(request,call_next):
    started=time.perf_counter(); response=await call_next(request); elapsed=time.perf_counter()-started
    REQUEST_COUNT.labels(request.url.path,request.method,response.status_code).inc(); REQUEST_LATENCY.labels(request.url.path).observe(elapsed)
    return response

@app.get("/health")
def health()->dict[str,Any]: return {"status":"healthy","service":APP_NAME,"model_version":MODEL_VERSION}

@app.get("/ready")
def ready()->dict[str,Any]:
    database_ok=db_healthcheck()
    return {"status":"ready" if database_ok else "degraded","database":database_ok,"model_version":MODEL_VERSION}

@app.get("/model")
def model_info(): return {"model_name":"news-ranking-model","model_version":MODEL_VERSION}

@app.post("/recommend",response_model=RecommendationResponse)
def recommend(request:RecommendationRequest):
    key=f"recommend:{MODEL_VERSION}:{request.user_id}:{request.category}:{request.top_k}"
    cached=get_cached(key)
    if cached is not None:
        CACHE_HIT_COUNT.inc(); return RecommendationResponse(**cached,cached=True)
    recommendations=generate_recommendations(request); RECOMMENDATION_COUNT.labels(MODEL_VERSION).inc(len(recommendations))
    payload={"user_id":request.user_id,"model_version":MODEL_VERSION,"recommendations":[x.model_dump() for x in recommendations]}
    set_cached(key,payload); return RecommendationResponse(**payload,cached=False)

@app.post("/rank",response_model=list[RecommendationItem])
def rank(items:list[RecommendationItem]):
    if not items: raise HTTPException(status_code=400,detail="items must not be empty")
    return sorted(items,key=lambda x:x.score,reverse=True)

@app.get("/metrics")
def metrics(): return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
