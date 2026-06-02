# Primordial VF Architecture

## 1. What We Are Building

Primordial VF, also called Voice Forge, is a style transformation system for rewriting text in the voice of a selected source corpus.

The core promise is simple:

- a user uploads writing they admire
- the system extracts the style structure from that writing
- the user later gives it new text to transform
- the system rewrites that text using the captured style

The product is therefore not just a retrieval system. It is a voice capture and voice application engine.

## 2. Core Product Idea

Primordial VF treats style as a first-class data object.

Instead of asking the model to "sound like" something through prompting alone, the system extracts measurable stylistic features from source text and stores them as reusable style anchors.

A style anchor includes:

- raw sample chunks
- sentence rhythm patterns
- punctuation habits
- paragraph shape
- register
- rhetorical patterns
- other structural signals that make a voice recognizable

The system later retrieves those anchors and uses them to steer generation.

## 3. Main Runtime Components

### 3.1 FastAPI API Layer

The API is the external entry point for the system.

It provides endpoints for:

- ingesting style source material
- ingesting optional factual knowledge later
- generating transformed output

The API layer is responsible for request validation, response formatting, and startup wiring.

### 3.2 Style Ingestion Layer

The style ingester is the core product primitive.

It takes uploaded writing and turns it into structured style memory by:

- chunking the source text
- extracting linguistic telemetry
- generating embeddings
- storing the chunks and metadata in Qdrant

This layer defines the quality of the style anchor the rest of the system will rely on.

### 3.3 LangGraph Orchestration Layer

LangGraph controls the generation pipeline.

It manages a typed state object through a sequence of nodes such as:

- validate input
- retrieve style anchor
- compile style context
- synthesize rewritten output

This gives us a deterministic and inspectable execution path.

### 3.4 Qdrant Cloud Storage Layer

Qdrant Cloud stores all embedded chunks in one collection.

For the style-first MVP, the collection primarily holds style anchors and their payload metadata.

The collection may also later hold factual knowledge, but the first product value is style retrieval.

Important payload fields include:

- `source_type`
- `style_anchor_id`
- `chunk_text`
- `telemetry`
- `chunk_index`
- `created_at`

### 3.5 Linguistic Telemetry Layer

Style anchors are not stored only as raw text.

They are also parsed into a structural fingerprint that captures traits such as:

- average sentence length
- sentence length distribution
- comma density
- em dash density
- paragraph brevity
- rhetorical devices
- register
- dominant mood

This telemetry is used as a blueprint during rewriting.

### 3.6 Groq Inference Layer

Groq handles the final text generation step.

It receives:

- the user’s new source text
- the selected style anchor chunks
- the extracted telemetry blueprint
- any optional rewrite instructions from the user

Its role is to generate transformed output that preserves the target voice patterns.

## 4. Data Flow

The system follows this path:

1. The user uploads a style source document.
2. The API validates the request.
3. The style ingester chunks and embeds the source text.
4. Linguistic telemetry is extracted from the source.
5. The style anchor is stored in Qdrant Cloud.
6. When the user wants a rewrite, the API sends the request into LangGraph.
7. LangGraph retrieves the selected style anchor.
8. The context compiler assembles raw style samples and telemetry.
9. The synthesis node sends the assembled prompt to Groq.
10. Groq returns rewritten text in the selected style.
11. The API returns the transformed output to the client.

## 5. State Shape

The LangGraph state should carry the minimum information needed to move through the pipeline:

- `user_query`
- `style_anchor_id`
- `input_text`
- `style_chunks`
- `telemetry_blueprint`
- `generation`
- `error`

If factual grounding is added later, the state can expand to include knowledge retrieval fields.

## 6. Project Structure

The scaffold is organized by responsibility:

- `primordial_vf/api`
  - FastAPI app, routes, and request/response schemas
- `primordial_vf/graph`
  - LangGraph state, graph factory, and node implementations
- `primordial_vf/models`
  - Pydantic models for telemetry and payloads
- `primordial_vf/storage`
  - Qdrant client and embedding abstraction
- `primordial_vf/llm`
  - Groq model access
- `primordial_vf/ingest`
  - Style and knowledge ingestion logic
- `scripts`
  - bootstrap, seeding, and smoke-test scripts
- `tests`
  - unit and integration coverage

## 7. Environment and Configuration

The project is configured through environment variables:

- `QDRANT_URL`
- `QDRANT_API_KEY`
- `QDRANT_COLLECTION`
- `GROQ_API_KEY`

These belong in `.env` locally and `.env.example` as the template.

## 8. MVP Boundaries

The MVP is intentionally focused on style transformation.

In scope:

- Qdrant Cloud-based storage
- style ingestion
- telemetry extraction
- style retrieval
- LangGraph orchestration
- Groq synthesis
- FastAPI endpoints
- CLI smoke test

Deferred for later:

- full knowledge grounding
- authentication
- multi-tenancy
- streaming responses
- dashboarding
- Docker-based deployment
- production observability stack

## 9. Validation Strategy

The architecture is validated by proving three things:

- style anchors are extracted faithfully
- style anchors are retrieved correctly
- changing the style anchor changes the output voice

The success condition is not just that the system runs. It is that the system can reliably capture and reproduce a recognizable writing voice.