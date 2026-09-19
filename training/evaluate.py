from __future__ import annotations

import json
from pathlib import Path


def ndcg_at_k(relevances: list[float], k: int = 10) -> float:
    values = relevances[:k]
    dcg = sum(rel / (__import__("math").log2(i + 2)) for i, rel in enumerate(values))
    ideal = sorted(relevances, reverse=True)[:k]
    idcg = sum(rel / (__import__("math").log2(i + 2)) for i, rel in enumerate(ideal))
    return float(dcg / idcg) if idcg else 0.0


def main() -> None:
    output = Path("artifacts/evaluation/metrics.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    metrics = {
        "precision_at_10": 0.0,
        "recall_at_10": 0.0,
        "ndcg_at_10": ndcg_at_k([]),
        "mrr": 0.0,
        "coverage": 0.0,
        "diversity": 0.0,
    }
    output.write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
