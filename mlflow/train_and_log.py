from __future__ import annotations

import os
from datetime import datetime

import mlflow

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("ipPrint-news-recommendation")

with mlflow.start_run(run_name=f"baseline-{datetime.utcnow():%Y%m%d-%H%M%S}"):
    mlflow.log_params({"model_type": "baseline", "top_k": 10})
    # Replace these placeholders with the metrics emitted by the existing
    # learning-to-rank evaluation pipeline.
    mlflow.log_metrics(
        {
            "precision_at_10": 0.0,
            "recall_at_10": 0.0,
            "ndcg_at_10": 0.0,
            "mrr": 0.0,
        }
    )
    mlflow.set_tag("stage", "development")
    print("MLflow run logged.")
