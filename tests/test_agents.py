from unittest.mock import patch

from src.agents.human_review_agent import needs_human_review
from src.agents.triage_graph import TriageGraph


def test_needs_human_review():
    assert needs_human_review("P1", 0.2)
    assert needs_human_review("P2", 0.8)
    assert not needs_human_review("P2", 0.5)


def test_triage_graph_flow():
    ticket = type("Ticket", (), {
        "ticket_id": "INC-2031",
        "title": "Test",
        "description": "Test description",
        "priority": "P1",
    })

    with patch("src.agents.triage_graph.classify_ticket", return_value="Data Engineering"), \
         patch("src.agents.triage_graph.predict_escalation_risk", return_value={"risk_score": 0.8}), \
         patch("src.agents.triage_graph.retrieve_similar_incidents", return_value=[]), \
         patch("src.agents.triage_graph.recommend_resolution", return_value={
             "assigned_team": "Data Platform",
             "recommended_resolution": "Test",
             "next_action": "Escalate",
         }):
        graph = TriageGraph()
        result = graph.run(ticket)
        assert result.category == "Data Engineering"
        assert result.escalation_required is True
        assert result.assigned_team == "Data Platform"
