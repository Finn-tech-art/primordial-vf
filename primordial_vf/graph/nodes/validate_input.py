from __future__ import annotations

from primordial_vf.graph.state import VFState
from primordial_vf.storage.embedder import get_embedder


def validate_input_node(state: VFState) -> VFState:
    """Validate generation input and create a retrieval vector."""
    style_anchor_id = state.get("style_anchor_id", "").strip()
    input_text = state.get("input_text", "").strip()

    if not style_anchor_id:
        return {"error": "style_anchor_id is required."}

    if not input_text:
        return {"error": "input_text is required."}

    query_text = state.get("rewrite_instruction") or input_text
    query_vector = get_embedder().embed_text(query_text)

    return {
        "style_anchor_id": style_anchor_id,
        "input_text": input_text,
        "rewrite_instruction": state.get("rewrite_instruction", ""),
        "query_vector": query_vector,
        "style_chunks": [],
    }
