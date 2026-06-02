from __future__ import annotations

import json

from primordial_vf.graph.state import VFState


def compile_context_node(state: VFState) -> VFState:
    """Compile style samples, telemetry, and user text into prompt context."""
    if state.get("error"):
        return {}

    style_chunks = state.get("style_chunks", [])
    telemetry_blueprint = state.get("telemetry_blueprint", {})

    if not style_chunks:
        return {"error": "No style chunks were retrieved for this style anchor."}

    compiled_prompt = build_generation_prompt(
        input_text=state.get("input_text", ""),
        rewrite_instruction=state.get("rewrite_instruction", ""),
        style_chunks=style_chunks,
        telemetry_blueprint=telemetry_blueprint,
    )

    return {"compiled_prompt": compiled_prompt}


def build_generation_prompt(
    input_text: str,
    rewrite_instruction: str,
    style_chunks: list[str],
    telemetry_blueprint: dict,
) -> str:
    """Build the final generation prompt."""
    style_samples = "\n\n---\n\n".join(style_chunks)

    instruction = rewrite_instruction.strip() or (
        "Rewrite the input text using the retrieved style anchor."
    )

    telemetry_json = json.dumps(telemetry_blueprint, indent=2, ensure_ascii=False)

    return f"""
You are Primordial VF, a voice transformation engine.

Your task is to rewrite the user's input text using the style evidence below.

You must preserve the meaning and intent of the input text.
You must not copy phrases from the style samples unless they are generic language.
You must use the style samples only as evidence of rhythm, structure, diction, and punctuation behavior.
You must not mention the source author or source material.

== STYLE TELEMETRY ==
{telemetry_json}

== STYLE SAMPLES ==
{style_samples}

== REWRITE INSTRUCTION ==
{instruction}

== INPUT TEXT ==
{input_text}

Return only the rewritten text.
""".strip()
