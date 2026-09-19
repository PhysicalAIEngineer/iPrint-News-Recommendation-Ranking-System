from __future__ import annotations

import os
import time
from typing import Any

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://api:8000")

st.set_page_config(
    page_title="iPrint Recommendation Intelligence",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    .hero {
        padding: 1.2rem 1.4rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        margin-bottom: 1rem;
    }
    .hero h1 { margin: 0; font-size: 2.2rem; }
    .hero p { margin: 0.4rem 0 0; color: #cbd5e1; }
    .article-card {
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        background: #ffffff;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.06);
    }
    .rank { font-size: 1.1rem; font-weight: 700; color: #475569; }
    .score { float: right; font-weight: 700; }
    .muted { color: #64748b; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>📰 iPrint Recommendation Intelligence</h1>
      <p>End-to-end news recommendation, ranking analytics, ML lifecycle, and production monitoring.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Control Center")
    page = st.radio(
        "Dashboard",
        ["Overview", "Live Recommendations", "Ranking Analytics", "Model & MLflow", "Monitoring"],
    )
    st.divider()
    st.caption(f"API endpoint: {API_URL}")

@st.cache_data(ttl=10)
def fetch_json(path: str) -> dict[str, Any] | None:
    try:
        response = requests.get(f"{API_URL}{path}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

@st.cache_data(ttl=2)
def recommend(user_id: str, category: str, top_k: int) -> dict[str, Any]:
    response = requests.post(
        f"{API_URL}/recommend",
        json={"user_id": user_id, "category": category, "top_k": top_k},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

health = fetch_json("/health")
model_info = fetch_json("/model")

api_status = "Online" if health else "Offline"
model_version = (model_info or {}).get("model_version", "unknown")

if page == "Overview":
    st.subheader("System Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("API Status", api_status)
    c2.metric("Model Version", model_version)
    c3.metric("Recommendation Engine", "Active" if health else "Unavailable")
    c4.metric("Observability", "Prometheus")

    st.divider()
    st.markdown("### Production Architecture")

    arch = pd.DataFrame(
        {
            "Layer": [
                "Data",
                "ML",
                "Model Registry",
                "Serving",
                "Cache",
                "Dashboard",
                "Monitoring",
            ],
            "Component": [
                "Transactions + Content",
                "Candidate Generation + LTR",
                "MLflow",
                "FastAPI",
                "Redis",
                "Streamlit",
                "Prometheus + Grafana",
            ],
        }
    )
    st.dataframe(arch, hide_index=True, use_container_width=True)

    st.markdown("### Recommendation Pipeline")
    st.code(
        "User → Candidate Generation → Semantic Retrieval → Learning-to-Rank → "
        "Recommendation API → Redis Cache → Dashboard",
        language="text",
    )

elif page == "Live Recommendations":
    st.subheader("Live Recommendation Explorer")
    st.caption("Use this page for the main product demonstration.")

    left, right = st.columns([1, 2])
    with left:
        user_id = st.text_input("User ID", "user-1024")
        category = st.selectbox(
            "News Category",
            ["general", "technology", "business", "sports", "science", "world"],
        )
        top_k = st.slider("Top-K Recommendations", 3, 20, 10)
        run = st.button("Generate Recommendations", type="primary", use_container_width=True)

    if run:
        start = time.perf_counter()
        payload = recommend(user_id, category, top_k)
        latency_ms = (time.perf_counter() - start) * 1000
        st.session_state["last_latency_ms"] = latency_ms
        st.session_state["last_payload"] = payload

    payload = st.session_state.get("last_payload")
    if payload:
        latency_ms = st.session_state.get("last_latency_ms", 0.0)
        m1, m2, m3 = st.columns(3)
        m1.metric("Model", payload["model_version"])
        m2.metric("Returned", len(payload["recommendations"]))
        m3.metric("Client Latency", f"{latency_ms:.1f} ms")

        with right:
            st.markdown("### Recommended Stories")
            for idx, item in enumerate(payload["recommendations"], start=1):
                st.markdown(
                    f"""
                    <div class="article-card">
                        <span class="rank">#{idx} · {item['article_id']}</span>
                        <span class="score">{item['score']:.4f}</span>
                        <div style="margin-top:0.45rem;font-size:1.05rem;font-weight:600">{item['title']}</div>
                        <div class="muted">Model: {item['model_version']} · Category: {category}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("### Ranking Distribution")
        rec_df = pd.DataFrame(payload["recommendations"])
        fig = px.bar(rec_df, x="article_id", y="score", title="Recommendation Scores", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Raw API Response"):
            st.json(payload)
    else:
        st.info("Enter a user and click Generate Recommendations.")

elif page == "Ranking Analytics":
    st.subheader("Ranking & Evaluation Analytics")

    metrics = pd.DataFrame(
        {
            "Metric": [
                "Precision@10",
                "Recall@10",
                "NDCG@10",
                "MRR",
                "Coverage",
                "Diversity",
                "Novelty",
            ],
            "Value": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        }
    )

    c1, c2 = st.columns([1, 2])
    with c1:
        st.dataframe(metrics, hide_index=True, use_container_width=True)
    with c2:
        fig = px.bar(metrics, x="Metric", y="Value", title="Model Evaluation Metrics")
        fig.update_yaxes(range=[0, 1])
        st.plotly_chart(fig, use_container_width=True)

    st.warning(
        "The current API serves the repository's deterministic fallback adapter. "
        "Replace these placeholder evaluation values with metrics generated by the real LTR evaluation artifact."
    )

    st.markdown("### Supported Ranking Metrics")
    st.code(
        "Precision@K | Recall@K | NDCG@K | MRR | Coverage | Diversity | Novelty | CTR",
        language="text",
    )

elif page == "Model & MLflow":
    st.subheader("Model Lifecycle & MLflow")

    c1, c2, c3 = st.columns(3)
    c1.metric("Registered Model", "news-ranking-model")
    c2.metric("Current Version", model_version)
    c3.metric("Experiment", "iPrint-news-recommendation")

    st.markdown("### Lifecycle")
    lifecycle = pd.DataFrame(
        {
            "Stage": ["Development", "Validation", "Registry", "Serving"],
            "Status": ["Configured", "Configured", "Configured", "API Adapter"],
        }
    )
    st.dataframe(lifecycle, hide_index=True, use_container_width=True)

    st.markdown("### MLflow Command")
    st.code(
        "MLFLOW_TRACKING_URI=http://localhost:5000 "
        "python training/mlflow_train.py",
        language="bash",
    )

    st.markdown("### Experiment Parameters")
    st.json(
        {
            "model_type": "baseline / existing LTR model",
            "top_k": 10,
            "tracking": "MLflow",
            "serving": "FastAPI",
            "cache": "Redis",
        }
    )

elif page == "Monitoring":
    st.subheader("Production Monitoring")

    metrics_payload = None
    try:
        raw = requests.get(f"{API_URL}/metrics", timeout=5)
        raw.raise_for_status()
        metrics_payload = raw.text
    except requests.RequestException:
        pass

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("API", api_status)
    m2.metric("Model Loaded", "Yes" if model_info else "Unknown")
    m3.metric("Metrics Endpoint", "Available" if metrics_payload else "Unavailable")
    m4.metric("Cache Layer", "Redis")

    st.markdown("### Metrics Being Observed")
    monitoring_df = pd.DataFrame(
        {
            "Metric": [
                "HTTP request count",
                "Request latency",
                "Recommendation count",
                "Cache hits",
                "Model loaded state",
                "Database readiness",
            ],
            "Source": [
                "Prometheus",
                "Prometheus",
                "Prometheus",
                "Prometheus",
                "Prometheus",
                "FastAPI /ready",
            ],
        }
    )
    st.dataframe(monitoring_df, hide_index=True, use_container_width=True)

    if metrics_payload:
        with st.expander("Raw Prometheus Metrics"):
            st.code(metrics_payload[:12000], language="text")
    else:
        st.info("Prometheus metrics endpoint is not reachable from the dashboard.")
