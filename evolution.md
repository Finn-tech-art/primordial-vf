# Primordial VF Evolution

## 1. Where We Are

We are at the scaffold and architecture-definition stage.

The project structure exists, but the functional pipeline has not been implemented yet. What we have done so far is define the product direction and agree on the build workflow.

## 2. What Has Been Decided

The following decisions are now fixed:

- The project is called **Primordial VF / Voice Forge**
- The MVP is now **style-first**
- The system will use **Qdrant Cloud**
- The system will run through **FastAPI**
- Orchestration will be handled by **LangGraph**
- Generation will use **Groq**
- Style will be represented through **linguistic telemetry**
- The user workflow will follow a **manual file-paste engineering process**
  - I write the file contents here
  - you paste them into VS Code
  - I do not directly edit files unless you explicitly ask me to

## 3. Why the Direction Changed

The original shape of the system leaned more toward factual retrieval and dual-lane RAG.

We refined that direction because the real product value appears to be:

- upload writing you admire
- extract the style
- reuse that style on new text later

That makes the style ingester the center of the system, not an afterthought.

## 4. What Exists Right Now

The following items are in place:

- the project directory scaffold
- empty placeholder files for implementation
- short module-purpose docstrings in package `__init__.py` files
- `.env`
- `.env.example`

The scaffold includes placeholders for:

- API modules
- graph nodes
- telemetry and payload models
- Qdrant storage abstraction
- Groq client
- ingestion logic
- tests
- bootstrap scripts

## 5. What Has Not Been Built Yet

The following still needs implementation:

- `pyproject.toml`
- runtime code in `config.py`
- Qdrant client setup
- embedding wrapper
- telemetry schema
- style ingestion
- LangGraph state and nodes
- Groq generation client
- FastAPI routes and app wiring
- smoke test and integration tests

## 6. Current Architectural Direction

We are now building a **style transformation engine**.

That means the system should:

- accept source writing
- extract style structure from it
- store the style anchor in Qdrant
- retrieve that anchor later
- rewrite new user text in that style

Knowledge retrieval may be added later, but it is no longer the primary MVP center.

## 7. Immediate Next Step

The next sensible build step is to define the style ingester in detail.

After that, the order should be:

1. `models/telemetry.py`
2. `models/knowledge.py` or a style payload model
3. `storage/qdrant_client.py`
4. `storage/embedder.py`
5. `ingest/style_ingester.py`
6. `graph/state.py`
7. `graph/nodes/*`
8. `graph/graph.py`
9. `api/*`
10. tests and smoke script

## 8. Build Philosophy Going Forward

We are building this in a controlled sequence.

That means:

- define the structure first
- write the smallest useful implementation next
- verify behavior with tests and smoke checks
- only then move to the next layer

The goal is to keep the architecture legible and the implementation easy to reason about as it grows.

## 9. Working Agreement

Going forward, the shared workflow is:

- I explain what each file does
- I explain how it fits into the architecture
- I write the file content here
- you paste it into the local file in VS Code

That keeps the build transparent and lets you stay fully in control of the codebase.