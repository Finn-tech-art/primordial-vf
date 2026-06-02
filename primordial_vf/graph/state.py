from __future__ import annotations

import operator
from typing import Annotated, Any

from typing_extensions import TypedDict


class VFState(TypedDict, total=False):
    """Shared LangGraph state for the style transformation pipeline."""

    style_anchor_id: str
    input_text: str
    rewrite_instruction: str

    query_vector: list[float]
    style_chunks: Annotated[list[str], operator.add]
    telemetry_blueprint: dict[str, Any]
    compiled_prompt: str

    generation: str
    error: str