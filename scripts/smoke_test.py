from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from primordial_vf.graph.graph import build_graph


STYLE_ANCHOR_ID = "demo_literary_sparse"

INPUT_TEXT = """
The application helps creators rewrite rough drafts into scripts with a more
distinctive voice. A user can upload writing they admire, capture the style, and
then apply that style to new material without fine-tuning a model.
""".strip()


def main() -> None:
    """Run a graph-based style rewrite smoke test."""
    graph = build_graph()

    result = graph.invoke(
        {
            "style_anchor_id": STYLE_ANCHOR_ID,
            "input_text": INPUT_TEXT,
            "rewrite_instruction": "Transform this into sparse literary prose.",
        }
    )

    print("Running Primordial VF graph smoke test...")
    print(f"Style anchor: {STYLE_ANCHOR_ID}")

    if result.get("error"):
        raise SystemExit(f"Smoke test failed: {result['error']}")

    print("\nInput:")
    print(INPUT_TEXT)

    print("\nRetrieved style chunks:")
    print(len(result.get("style_chunks", [])))

    print("\nOutput:")
    print(result.get("generation", ""))


if __name__ == "__main__":
    main()