import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

import numpy as np
from sentence_transformers import SentenceTransformer

try:
    import faiss
except ImportError:
    faiss = None

from src.retrieval.vector_store import TicketVectorStore

MODEL_DIR = Path(os.getenv("MODEL_DIR", "./models"))
MODEL_DIR.mkdir(parents=True, exist_ok=True)
DATA_PATH = Path(os.getenv("TICKET_DATA_PATH", "./data/raw/sample_incidents.json"))
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
INDEX_PATH = MODEL_DIR / "faiss_index.index"
METADATA_PATH = MODEL_DIR / "ticket_metadata.json"


def load_tickets():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_ticket_embeddings():
    tickets = load_tickets()
    model = SentenceTransformer(EMBED_MODEL)
    texts = [f"{ticket['title']} {ticket['description']}" for ticket in tickets]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    if faiss is not None:
        faiss.normalize_L2(embeddings)
    else:
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    store = TicketVectorStore(str(INDEX_PATH), str(METADATA_PATH))
    store.build(embeddings, tickets)
    print(f"Built vector store with {len(tickets)} tickets")


if __name__ == "__main__":
    build_ticket_embeddings()
