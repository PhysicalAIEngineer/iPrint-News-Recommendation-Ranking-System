import os,json
from datetime import datetime,timezone
from pathlib import Path
import mlflow
def main():
 mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI","http://localhost:5000"))
 mlflow.set_experiment("iPrint-news-recommendation")
 with mlflow.start_run(run_name=f"baseline-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}"):
  mlflow.log_params({"model_type":"baseline","top_k":10})
  p=Path("artifacts/evaluation/metrics.json")
  metrics=json.loads(p.read_text()) if p.exists() else {"precision_at_10":0.0,"recall_at_10":0.0,"ndcg_at_10":0.0,"mrr":0.0}
  mlflow.log_metrics({k:float(v) for k,v in metrics.items() if isinstance(v,(int,float))})
  mlflow.set_tag("stage","development")
if __name__=="__main__": main()