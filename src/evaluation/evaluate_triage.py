import json
import os
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.models.predict import predict_category, predict_risk
from src.retrieval.similar_ticket_search import find_similar_incidents

DATA_PATH = Path(os.getenv("TICKET_DATA_PATH", "./data/raw/sample_incidents.json"))
REPORT_PATH = Path(__file__).resolve().parent / "metrics_report.md"


def load_dataset():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate():
    tickets = load_dataset()
    categories = [ticket["category"] for ticket in tickets]
    preds = [predict_category(ticket["title"], ticket["description"]) for ticket in tickets]

    risk_labels = [1 if ticket["priority"] == "P1" or ticket["category"] in {"Security Alert", "Database", "Deployment Failure"} else 0 for ticket in tickets]
    risk_preds = [predict_risk(ticket["priority"], ticket["category"], ticket["description"])["risk_score"] >= 0.75 for ticket in tickets]

    latency_samples = []
    retrieval_hits = []
    for ticket in tickets[:10]:
        start = time.time()
        try:
            hits = find_similar_incidents(ticket["title"], ticket["description"], top_k=3)
            retrieval_hits.append(any(hit["ticket_id"] != ticket["ticket_id"] for hit in hits))
        except Exception:
            retrieval_hits.append(False)
        latency_samples.append(time.time() - start)

    metrics = {
        "classification_accuracy": accuracy_score(categories, preds),
        "classification_precision": precision_score(categories, preds, average="weighted", zero_division=0),
        "classification_recall": recall_score(categories, preds, average="weighted", zero_division=0),
        "classification_f1": f1_score(categories, preds, average="weighted", zero_division=0),
        "risk_f1": f1_score(risk_labels, risk_preds),
        "similar_hit_rate": float(np.mean(retrieval_hits) if retrieval_hits else 0.0),
        "average_latency": float(np.mean(latency_samples) if latency_samples else 0.0),
        "human_review_routing_accuracy": float(
            np.mean([
                (ticket["priority"] == "P1" or predict_risk(ticket["priority"], ticket["category"], ticket["description"])["risk_score"] >= 0.75)
                == (ticket["priority"] == "P1" or ticket["category"] in {"Security Alert", "Database", "Deployment Failure"})
                for ticket in tickets
            ])
        ),
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as report:
        report.write("# Evaluation Metrics\n\n")
        for key, value in metrics.items():
            report.write(f"- **{key.replace('_', ' ').title()}:** {value:.2f}\n")
    print(f"Wrote evaluation report to {REPORT_PATH}")


if __name__ == "__main__":
    evaluate()
