from __future__ import annotations

from functools import lru_cache

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PayloadSchemaType, VectorParams

from primordial_vf.config import Settings, get_settings


@lru_cache
def get_qdrant_client() -> QdrantClient:
    """Return a cached Qdrant Cloud client."""
    settings = get_settings()
    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )


def init_collection(
    client: QdrantClient | None = None,
    settings: Settings | None = None,
    recreate: bool = False,
) -> None:
    """Create the Qdrant collection and payload indexes if needed."""
    settings = settings or get_settings()
    client = client or get_qdrant_client()

    collection_exists = client.collection_exists(settings.qdrant_collection)

    if recreate and collection_exists:
        client.delete_collection(collection_name=settings.qdrant_collection)
        collection_exists = False

    if not collection_exists:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=settings.embedding_dim,
                distance=Distance.COSINE,
            ),
        )

    ensure_payload_indexes(client=client, collection_name=settings.qdrant_collection)


def ensure_payload_indexes(client: QdrantClient, collection_name: str) -> None:
    """Create payload indexes used by style and future knowledge retrieval."""
    indexed_fields = {
        "source_type": PayloadSchemaType.KEYWORD,
        "style_anchor_id": PayloadSchemaType.KEYWORD,
        "user_id": PayloadSchemaType.KEYWORD,
    }

    for field_name, field_schema in indexed_fields.items():
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            field_schema=field_schema,
        )
