from unittest.mock import patch

from src.retrieval.similar_ticket_search import find_similar_incidents


def test_find_similar_incidents_with_dummy_store():
    dummy_hits = [
        {"ticket_id": "INC-1002", "title": "Airflow DAG failed after schema change", "similarity_score": 0.91, "resolution": "Updated dbt model."}
    ]

    class DummyStore:
        def __init__(self, index_path, metadata_path):
            pass

        def search(self, query_embedding, top_k=3):
            return [{"metadata": {"ticket_id": "INC-1002", "title": "Airflow DAG failed after schema change", "resolution": "Updated dbt model."}, "score": 0.91}]

    with patch("src.retrieval.similar_ticket_search.TicketVectorStore", DummyStore):
        with patch("src.retrieval.similar_ticket_search.SentenceTransformer") as DummyModel:
            DummyModel.return_value.encode.return_value = [[0.1, 0.2, 0.3]]
            results = find_similar_incidents("Test title", "Test description")
            assert isinstance(results, list)
            assert results[0]["ticket_id"] == "INC-1002"
