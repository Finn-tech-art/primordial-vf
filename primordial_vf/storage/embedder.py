from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from primordial_vf.config import get_settings


class Embedder:
    """Small wrapper around SentenceTransformers embeddings."""

    def __init__(self, model_name: str) -> None:
        self._model = SentenceTransformer(model_name, trust_remote_code=True)

    def embed_text(self, text: str) -> list[float]:
        """Embed a single text string."""
        vector = self._model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple text strings."""
        if not texts:
            return []

        vectors = self._model.encode(texts, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]


@lru_cache
def get_embedder() -> Embedder:
    """Return a cached embedder instance."""
    settings = get_settings()
    return Embedder(settings.embedding_model)