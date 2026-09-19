import os

import pandas as pd
import streamlit as st

API_URL = os.getenv("API_URL", "http://api:8000")

st.set_page_config(page_title="iPrint Recommendation Dashboard", layout="wide")
st.title("iPrint News Recommendation System")
st.caption("Recommendation analytics and serving dashboard")

c1, c2, c3, c4 = st.columns(4)
c1.metric("API", "Online")
c2.metric("Model", os.getenv("MODEL_VERSION", "baseline-v1"))
c3.metric("Top-K", 10)
c4.metric("Monitoring", "Prometheus")

st.subheader("Generate Recommendations")
user_id = st.text_input("User ID", "demo-user")
category = st.selectbox("Category", ["general", "technology", "business", "sports", "science"])
top_k = st.slider("Top-K", 1, 20, 10)

if st.button("Recommend"):
    import requests
    response = requests.post(
        f"{API_URL}/recommend",
        json={"user_id": user_id, "category": category, "top_k": top_k},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    st.success(f"Model: {payload['model_version']}")
    rows = [
        {
            "Rank": i + 1,
            "Article ID": x["article_id"],
            "Title": x["title"],
            "Score": x["score"],
        }
        for i, x in enumerate(payload["recommendations"])
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.subheader("Evaluation Metrics")
metric_df = pd.DataFrame(
    {
        "Metric": ["Precision@10", "Recall@10", "NDCG@10", "MRR", "Coverage", "Diversity"],
        "Value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    }
)
st.dataframe(metric_df, use_container_width=True, hide_index=True)

st.info("Populate live evaluation values from MLflow runs or persisted evaluation artifacts.")
