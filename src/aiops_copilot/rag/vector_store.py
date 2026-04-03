from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class SearchHit:
    score: float
    payload: dict[str, Any]


class LocalVectorStore:
    def __init__(self, index_path: str, metadata_path: str, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.model = SentenceTransformer(model_name)
        self.index: faiss.IndexFlatIP | None = None
        self.metadata: list[dict[str, Any]] = []
        self._bootstrap()

    def _bootstrap(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        if self.index_path.exists() and self.metadata_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            self.metadata = json.loads(self.metadata_path.read_text())
            return
        emb_dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(emb_dim)
        self._flush()

    def _flush(self) -> None:
        assert self.index is not None
        faiss.write_index(self.index, str(self.index_path))
        self.metadata_path.write_text(json.dumps(self.metadata, indent=2))

    def upsert(self, texts: list[str], payloads: list[dict[str, Any]]) -> int:
        assert self.index is not None
        vectors = self.model.encode(texts, normalize_embeddings=True)
        matrix = np.array(vectors, dtype=np.float32)
        self.index.add(matrix)
        self.metadata.extend(payloads)
        self._flush()
        return len(texts)

    def search(self, query: str, k: int = 6) -> list[SearchHit]:
        assert self.index is not None
        if self.index.ntotal == 0:
            return []
        q_vec = self.model.encode([query], normalize_embeddings=True)
        q_matrix = np.array(q_vec, dtype=np.float32)
        scores, indices = self.index.search(q_matrix, k)
        hits: list[SearchHit] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            hits.append(SearchHit(score=float(score), payload=self.metadata[idx]))
        return hits
