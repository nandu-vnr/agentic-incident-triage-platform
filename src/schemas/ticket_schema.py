from pydantic import BaseModel
from typing import List, Optional, Literal

class IncidentTicket(BaseModel):
    ticket_id: str
    title: str
    description: str
    priority: Literal["P1", "P2", "P3", "P4"]

class SimilarIncident(BaseModel):
    ticket_id: str
    title: str
    similarity_score: float
    resolution: str

class TriageResponse(BaseModel):
    category: str
    sub_category: Optional[str]
    urgency: Literal["Low", "Medium", "High", "Critical"]
    escalation_required: bool
    risk_score: float
    assigned_team: str
    similar_incidents: List[SimilarIncident]
    recommended_resolution: str
    next_action: str
