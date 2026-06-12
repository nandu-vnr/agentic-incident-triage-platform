import json
import os
from pathlib import Path
from typing import List, Dict

import numpy as np

try:
    import faiss
except ImportError:
    faiss = None


class TicketVectorStore:
    def __init__(self, index_path: str, metadata_path: str):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.metadata: List[Dict] = []
        self.index = None
        self._load()

    def _load(self):
        if self.metadata_path.exists():
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

        if faiss is not None and self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        elif self.index_path.with_suffix(".npy").exists():
            self.index = np.load(self.index_path.with_suffix(".npy"))

    def build(self, embeddings: np.ndarray, metadata: List[Dict]):
        self.metadata = metadata
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

        if faiss is None:
            self.index = embeddings
            np.save(self.index_path.with_suffix(".npy"), embeddings)
        else:
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)
            faiss.normalize_L2(embeddings)
            self.index.add(embeddings)
            faiss.write_index(self.index, str(self.index_path))

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        if self.index is None:
            raise RuntimeError("Vector index not loaded")

        if faiss is None:
            embeddings = self.index
            query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
            similarities = embeddings @ query_embedding.T
            idx = np.argsort(-similarities.ravel())[:top_k]
            results = similarities.ravel()[idx]
        else:
            faiss.normalize_L2(query_embedding)
            results, idx = self.index.search(query_embedding, top_k)
            idx = idx.ravel()
            results = results.ravel()

        hits = []
        for score, row_idx in zip(results, idx):
            if row_idx < 0 or row_idx >= len(self.metadata):
                continue
            hits.append({
                "metadata": self.metadata[row_idx],
                "score": float(score),
            })
        return hits
