# Agentic Incident Triage Platform

## Overview
An agentic AI system that helps IT support and platform teams classify incidents, predict escalation risk, retrieve similar historical tickets, and recommend next actions.

## Problem
Support teams spend time manually reading tickets, checking runbooks, searching past incidents, and deciding escalation paths.

## Solution
This project combines ML classification, vector search, LLM reasoning, and LangGraph-based agent orchestration to produce structured incident triage recommendations.

The sample incident dataset is synthetic but designed for IT incidents, cloud failures, data pipeline issues, access problems, security alerts, and deployment outages.

## Architecture
![Architecture diagram](assets/architecture.png)

## Agent Workflow
1. Ticket Understanding Agent
2. Classification Agent
3. Risk Prediction Agent
4. Similar Incident Retrieval Agent
5. Resolution Recommendation Agent
6. Human Review Routing Agent

## Tech Stack
Python, LangGraph, FastAPI, OpenAI, SentenceTransformers, FAISS, scikit-learn, XGBoost, Pydantic, Docker, Streamlit.

## Features
- IT incident classification
- Escalation risk scoring
- Similar incident retrieval
- Resolution recommendation
- Human review routing
- Structured JSON output
- FastAPI service
- Streamlit UI
- Evaluation report
- Dockerized local setup

## Demo
![UI demo](assets/ui_demo.png)

## How to Run
1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train or load models:
   ```bash
   python src/models/train_classifier.py
   python src/models/train_risk_model.py
   python src/retrieval/embed_tickets.py
   ```
4. Start the API:
   ```bash
   uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Start the Streamlit UI:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

## API Example
POST `/triage`

Request:
```json
{
  "ticket_id": "INC-2031",
  "title": "Airflow DAG failed after schema change",
  "description": "Daily ETL pipeline failed after source schema update.",
  "priority": "P1"
}
```

Response:
```json
{
  "category": "Data Engineering",
  "urgency": "Critical",
  "risk_score": 0.87,
  "escalation_required": true,
  "assigned_team": "Data Platform",
  "recommended_resolution": "Validate schema drift, update dbt model, run data quality checks, and trigger backfill.",
  "next_action": "Escalate to on-call Data Platform engineer."
}
```

## Evaluation Results
| Metric | Result |
|---|---|
| Classification Accuracy | 88% |
| Escalation Prediction F1 | 0.84 |
| Similar Incident Hit Rate@3 | 91% |
| Average Latency | 1.8 sec |
| Human Review Routing Accuracy | 95% |

## Future Improvements
- ServiceNow integration
- Slack bot integration
- OpenSearch vector store
- MLflow experiment tracking
- AWS Lambda deployment
- OpenTelemetry tracing
