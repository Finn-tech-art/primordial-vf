from __future__ import annotations

import argparse
import sys
from pathlib import Path

from qdrant_client.http.exceptions import UnexpectedResponse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from primordial_vf.config import get_settings
from primordial_vf.storage.qdrant_client import get_qdrant_client, init_collection


def main() -> None:
    """Initialize the Qdrant Cloud collection used by Primordial VF."""
    parser = argparse.ArgumentParser(description="Initialize the Qdrant collection.")
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete and recreate the collection before adding indexes.",
    )
    args = parser.parse_args()

    settings = get_settings()
    client = get_qdrant_client()

    print(f"Qdrant URL: {settings.qdrant_url}")
    print(f"Collection: {settings.qdrant_collection}")
    print(f"Embedding dim: {settings.embedding_dim}")

    try:
        init_collection(
            client=client,
            settings=settings,
            recreate=args.recreate,
        )
    except UnexpectedResponse as exc:
        raise SystemExit(f"Qdrant initialization failed: {exc}") from exc

    print("Qdrant collection is ready.")


if __name__ == "__main__":
    main()