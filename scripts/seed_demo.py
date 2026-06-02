from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from primordial_vf.ingest.style_ingester import StyleIngester


DEMO_STYLE_TEXT = """
The room was quiet, but not empty.

Something had been said there. Something heavy enough to stay behind after the
voices left. The table held its little evidence: a glass ring, a folded receipt,
a pen with no cap. Ordinary things. Accusing things.

Mara stood by the window and watched the street gather itself into evening. Cars
moved below in patient lines. A man crossed against the light and did not hurry.
The city had a way of continuing. That was the cruelest part.

She read the message again.

No apology. No explanation. Just seven words, each one placed with surgical care.

I did what you asked me to do.

For a while, she hated him for the sentence. Then she hated herself for
understanding it.
""".strip()


def main() -> None:
    """Seed one demo style anchor into Qdrant."""
    ingester = StyleIngester()

    result = ingester.ingest(
        style_anchor_id="demo_literary_sparse",
        text=DEMO_STYLE_TEXT,
        metadata={
            "label": "Demo literary sparse style",
            "source": "local demo seed",
        },
    )

    print("Style anchor ingested.")
    print(f"Style anchor ID: {result.style_anchor_id}")
    print(f"Chunks stored: {result.chunks_stored}")
    print(f"Collection: {result.collection}")
    print("Telemetry:")
    print(json.dumps(result.telemetry.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    main()