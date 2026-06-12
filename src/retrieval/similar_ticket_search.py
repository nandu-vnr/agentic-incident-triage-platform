import os
import sys
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

import numpy as np
from sentence_transformers import SentenceTransformer

from src.retrieval.vector_store import TicketVectorStore

MODEL_DIR = Path(os.getenv("MODEL_DIR", "./models"))
INDEX_PATH = MODEL_DIR / "faiss_index.index"
METADATA_PATH = MODEL_DIR / "ticket_metadata.json"
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


def find_similar_incidents(title: str, description: str, top_k: int = 3) -> List[dict]:
    store = TicketVectorStore(str(INDEX_PATH), str(METADATA_PATH))
    if store.index is None:
        raise RuntimeError("No vector store available. Run src/retrieval/embed_tickets.py first.")

    model = SentenceTransformer(EMBED_MODEL)
    query_embedding = model.encode([f"{title} {description}"], convert_to_numpy=True)
    query_embedding = query_embedding.astype('float32')
    results = store.search(query_embedding, top_k=top_k)
    return [
        {
            "ticket_id": hit["metadata"]["ticket_id"],
            "title": hit["metadata"]["title"],
            "similarity_score": round(hit["score"], 3),
            "resolution": hit["metadata"].get("resolution", ""),
        }
        for hit in results
    ]
