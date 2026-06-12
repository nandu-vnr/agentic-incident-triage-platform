import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.agents.triage_graph import TriageGraph
from src.schemas.ticket_schema import IncidentTicket
from src.utils.logger import logger

app = FastAPI(
    title="Agentic Incident Triage Platform",
    description="FastAPI service for IT incident triage with classification, risk scoring, retrieval, and resolution recommendations.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = TriageGraph()
DATA_PATH = os.getenv("TICKET_DATA_PATH", "./data/raw/sample_incidents.json")


@app.get("/health")
def health():
    return {"status": "ok", "service": "agentic-incident-triage"}


@app.get("/metrics")
def metrics():
    return {
        "service": "agentic-incident-triage",
        "ticket_data_path": DATA_PATH,
    }


@app.post("/triage")
def triage(ticket: IncidentTicket):
    logger.info(f"Received ticket {ticket.ticket_id}")
    response = workflow.run(ticket)
    return response
