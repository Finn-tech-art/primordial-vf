from __future__ import annotations

from qdrant_client.models import FieldCondition, Filter, MatchValue

from primordial_vf.config import get_settings
from primordial_vf.graph.state import VFState
from primordial_vf.storage.qdrant_client import get_qdrant_client


def retrieve_style_node(state: VFState) -> VFState:
    """Retrieve style samples and telemetry for the selected style anchor."""
    if state.get("error"):
        return {}

    settings = get_settings()
    client = get_qdrant_client()

    query_vector = state.get("query_vector")
    style_anchor_id = state.get("style_anchor_id")

    if not query_vector:
        return {"error": "query_vector is missing."}

    if not style_anchor_id:
        return {"error": "style_anchor_id is missing."}

    response = client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="source_type",
                    match=MatchValue(value="style_anchor"),
                ),
                FieldCondition(
                    key="style_anchor_id",
                    match=MatchValue(value=style_anchor_id),
                ),
            ]
        ),
        limit=5,
        with_payload=True,
    )

    style_chunks: list[str] = []
    telemetry_blueprint = None

    for point in response.points:
        payload = point.payload or {}

        chunk_text = payload.get("chunk_text")
        telemetry = payload.get("telemetry")

        if isinstance(chunk_text, str):
            style_chunks.append(chunk_text)

        if telemetry_blueprint is None and isinstance(telemetry, dict):
            telemetry_blueprint = telemetry

    if not style_chunks:
        return {"error": f"No style chunks found for style_anchor_id={style_anchor_id!r}."}

    return {
        "style_chunks": style_chunks,
        "telemetry_blueprint": telemetry_blueprint or {},
    }