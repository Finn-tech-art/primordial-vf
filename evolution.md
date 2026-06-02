```md
# Primordial VF Evolution

## 1. Current State

Primordial VF has moved from scaffold to first working output.

The system now has a functional style-first path:

```text
style ingestion -> Qdrant storage -> graph retrieval -> Groq rewrite
```

This is the first real proof that the architecture can run end to end.

## 2. Product Direction

The project started from a dual-lane RAG idea:

- factual retrieval
- stylistic retrieval

The direction has shifted to a style-first MVP.

The current product focus is:

- upload a writing sample
- extract its style
- store it as a reusable style anchor
- rewrite new text in that style

Knowledge ingestion and factual grounding remain possible future layers, but they are no longer the first product milestone.

## 3. What Is Working

The following pieces are now working:

- environment loading through `.env`
- Qdrant Cloud collection initialization
- Groq client setup
- Pydantic telemetry model
- style ingestion through `StyleIngester`
- Groq-powered telemetry extraction
- local embedding with SentenceTransformers
- Qdrant upsert of style chunks
- LangGraph graph construction
- graph-based smoke test
- Qdrant style retrieval through `query_points`
- Groq generation through the synthesis node

## 4. First Smoke Test Result

The demo style anchor was ingested successfully:

```text
Style anchor ID: demo_literary_sparse
Chunks stored: 1
Collection: vf_corpus
```

The graph smoke test also succeeded.

It retrieved one style chunk and produced a rewritten output.

## 5. What We Learned

The infrastructure works.

The current quality issue is not connectivity or orchestration. It is style fidelity.

The first generated output preserved meaning, but it leaned too formal and polished. It did not yet fully reproduce the sparse literary rhythm of the demo anchor.

This means the next work is prompt tuning and style-pressure design, not plumbing.

## 6. Current Known Issues

- `compile_context.py` needs stronger style instructions
- the generation prompt should discourage corporate/product language
- telemetry extraction is useful, but some hard metrics may need deterministic backup later
- `seed_demo.py` currently stores only one demo chunk because the sample is short
- FastAPI routes are not built yet
- Supabase is not wired yet
- knowledge ingestion is deferred

## 7. Next Engineering Step

The next file to improve is:

```text
primordial_vf/graph/nodes/compile_context.py
```

Goal:

- make the model apply the selected style more visibly
- preserve meaning
- avoid adding facts
- avoid generic marketing prose
- make output paragraph rhythm resemble the retrieved anchor

## 8. Future Milestones

Planned next milestones:

1. Tune the generation prompt for stronger style fidelity.
2. Add a second contrasting style anchor.
3. Compare two outputs from the same input using different anchors.
4. Move smoke test behavior into FastAPI routes.
5. Add tests around telemetry, chunking, retrieval, and graph behavior.
6. Add Supabase later for auth, files, metadata, and generation history.
7. Add optional knowledge ingestion for grounded factual generation.
8. Add a parallel Groq extraction swarm for higher-quality style analysis.
```