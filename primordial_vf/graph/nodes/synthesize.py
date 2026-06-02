from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from primordial_vf.graph.state import VFState
from primordial_vf.llm.groq_client import get_generation_llm


SYSTEM_PROMPT = """
You are a careful style transformation engine.

Preserve the user's meaning.
Apply the provided style evidence structurally.
Do not add facts.
Do not explain your process.
Return only the rewritten text.
""".strip()


def synthesize_node(state: VFState) -> VFState:
    """Generate the final rewritten text with Groq."""
    if state.get("error"):
        return {}

    compiled_prompt = state.get("compiled_prompt")

    if not compiled_prompt:
        return {"error": "compiled_prompt is missing."}

    response = get_generation_llm().invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=compiled_prompt),
        ]
    )

    return {"generation": str(response.content)}
