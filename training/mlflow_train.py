from __future__ import annotations

import os
from datetime import datetime, timezone

import mlflow

TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")


def main() -> None:
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment("iPrint-news-recommendation")

    with mlflow.start_run(
        run_name=f"baseline-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}"
    ):
        mlflow.log_params({"model_type": "baseline", "top_k": 10})
        mlflow.log_metrics(
            {
                "precision_at_10": 0.0,
                "recall_at_10": 0.0,
                "ndcg_at_10": 0.0,
                "mrr": 0.0,
            }
        )
        mlflow.set_tag("stage", "development")
        print("MLflow run logged successfully.")


if __name__ == "__main__":
    main()
