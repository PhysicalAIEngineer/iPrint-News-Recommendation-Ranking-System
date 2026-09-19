import json
import os
from datetime import datetime, timezone
from pathlib import Path

import mlflow


def main():
    mlflow.set_tracking_uri(
        os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    )
    mlflow.set_experiment("iPrint-news-recommendation")

    run_name = f"baseline-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}"
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params({"model_type": "baseline", "top_k": 10})

        metrics_path = Path("artifacts/evaluation/metrics.json")
        if metrics_path.exists():
            metrics = json.loads(metrics_path.read_text())
        else:
            metrics = {
                "precision_at_10": 0.0,
                "recall_at_10": 0.0,
                "ndcg_at_10": 0.0,
                "mrr": 0.0,
            }

        mlflow.log_metrics(
            {
                key: float(value)
                for key, value in metrics.items()
                if isinstance(value, (int, float))
            }
        )
        mlflow.set_tag("stage", "development")


if __name__ == "__main__":
    main()
