```md
# Primordial VF

Primordial VF, also called Voice Forge, is a style-first voice transformation system.

It lets a user upload writing with a style they admire, extracts a reusable style profile from that writing, stores it in Qdrant Cloud, and later rewrites new text using that captured style.

## Current Status

The first working graph smoke test is complete.

The system can currently:

- ingest a demo style source
- extract linguistic telemetry with Groq
- embed the style chunk
- store the style anchor in Qdrant Cloud
- retrieve the style anchor through LangGraph
- generate a rewritten output through Groq

The next engineering focus is improving style fidelity.

## Stack

- Python 3.11+
- uv
- Pydantic v2
- python-dotenv
- Qdrant Cloud
- SentenceTransformers
- LangGraph
- LangChain Groq
- Groq free-tier models

## Environment Variables

Create a `.env` file with:

```env
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION=vf_corpus

GROQ_API_KEY=

GROQ_GENERATION_MODEL=llama-3.3-70b-versatile
GROQ_EXTRACTION_MODEL=llama-3.1-8b-instant

EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
EMBEDDING_DIM=768

CHUNK_SIZE_WORDS=450
CHUNK_OVERLAP_WORDS=75
```

## Setup

Create and sync the environment:

```bash
uv sync
```

Initialize Qdrant Cloud:

```bash
uv run python scripts/init_qdrant.py
```

Ingest the demo style anchor:

```bash
uv run python scripts/seed_demo.py
```

Run the graph smoke test:

```bash
uv run python scripts/smoke_test.py
```

## Current Pipeline

```text
seed_demo.py
-> StyleIngester
-> Groq extraction
-> embedding
-> Qdrant Cloud

smoke_test.py
-> LangGraph
-> validate input
-> retrieve style
-> compile context
-> synthesize with Groq
-> output
```

## Current Demo Style Anchor

The demo style anchor is:

```text
demo_literary_sparse
```

It is a short literary sample designed to test:

- restrained prose
- short paragraph beats
- reflective mood
- concrete scene detail
- sparse dramatic pacing

## Current Known Limitation

The first generated output is coherent and meaning-preserving, but not yet stylistically strong enough.

The next improvement is to tune the generation prompt so the model follows the sparse literary style more aggressively and avoids polished product-language drift.
```
