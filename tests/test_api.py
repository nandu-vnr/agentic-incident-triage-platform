from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_triage_endpoint_with_mocked_workflow():
    mock_response = {
        "category": "Data Engineering",
        "sub_category": None,
        "urgency": "Critical",
        "escalation_required": True,
        "risk_score": 0.87,
        "assigned_team": "Data Platform",
        "similar_incidents": [],
        "recommended_resolution": "Test recommendation.",
        "next_action": "Escalate to on-call Data Platform engineer.",
    }
    with patch("src.api.main.workflow") as mock_workflow:
        mock_workflow.run.return_value = mock_response
        response = client.post(
            "/triage",
            json={
                "ticket_id": "INC-2031",
                "title": "Airflow DAG failed after schema change",
                "description": "Daily ETL pipeline failed after source schema update.",
                "priority": "P1",
            },
        )
        assert response.status_code == 200
        assert response.json()["category"] == "Data Engineering"
        assert response.json()["risk_score"] == 0.87
