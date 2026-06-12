from src.agents.classifier_agent import classify_ticket
from src.agents.risk_agent import predict_escalation_risk
from src.agents.retrieval_agent import retrieve_similar_incidents
from src.agents.resolution_agent import recommend_resolution
from src.agents.human_review_agent import needs_human_review
from src.schemas.ticket_schema import TriageResponse, SimilarIncident


class TriageGraph:
    def __init__(self):
        self.nodes = [
            "parse_ticket",
            "classify_ticket",
            "predict_escalation_risk",
            "retrieve_similar_incidents",
            "recommend_resolution",
            "check_human_review",
        ]

    def run(self, ticket):
        category = classify_ticket(ticket)
        risk = predict_escalation_risk(ticket, category)
        similar_incidents = retrieve_similar_incidents(ticket)
        recommendation = recommend_resolution(ticket, category, risk["risk_score"], similar_incidents)
        escalate = needs_human_review(ticket.priority, risk["risk_score"])

        urgency = "Critical" if ticket.priority == "P1" or risk["risk_score"] >= 0.85 else (
            "High" if risk["risk_score"] >= 0.6 else "Medium"
        )

        return TriageResponse(
            category=category,
            sub_category=None,
            urgency=urgency,
            escalation_required=escalate,
            risk_score=risk["risk_score"],
            assigned_team=recommendation["assigned_team"],
            similar_incidents=[
                SimilarIncident(
                    ticket_id=item["ticket_id"],
                    title=item["title"],
                    similarity_score=item["similarity_score"],
                    resolution=item["resolution"],
                )
                for item in similar_incidents
            ],
            recommended_resolution=recommendation["recommended_resolution"],
            next_action=recommendation["next_action"],
        )
