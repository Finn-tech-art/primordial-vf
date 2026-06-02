from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from primordial_vf.config import Settings, get_settings
from primordial_vf.llm.groq_client import get_extraction_llm
from primordial_vf.models.telemetry import LinguisticTelemetry, StyleAnchorPayload
from primordial_vf.storage.embedder import Embedder, get_embedder
from primordial_vf.storage.qdrant_client import get_qdrant_client


STYLE_EXTRACTION_SYSTEM_PROMPT = """
You are a linguistic style analyst for a voice transformation system.

Your task is to analyze the supplied writing sample for style, not meaning.

Return a structured linguistic fingerprint that describes how the text is written:
sentence rhythm, paragraph shape, punctuation behavior, style register, narrative
posture, rhetorical devices, and stylistic notes.

Do not summarize the plot, argument, topic, or factual content.
Do not imitate the author.
Do not identify copyrighted authors by name.
Focus only on reusable linguistic structure.
""".strip()


STYLE_EXTRACTION_HUMAN_PROMPT = """
Analyze this writing sample as a style source.

The values must describe the sample itself, not an idealized version of it.

Writing sample:

{text}
""".strip()


@dataclass(frozen=True)
class StyleIngestResult:
    """Summary returned after ingesting a style anchor."""

    style_anchor_id: str
    chunks_stored: int
    telemetry: LinguisticTelemetry
    collection: str


class StyleIngester:
    """Ingest source writing as reusable style memory."""

    def __init__(
        self,
        qdrant_client: QdrantClient | None = None,
        embedder: Embedder | None = None,
        extraction_llm: BaseChatModel | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.qdrant_client = qdrant_client or get_qdrant_client()
        self.embedder = embedder or get_embedder()
        self.extraction_llm = extraction_llm or get_extraction_llm()

    def ingest(
        self,
        style_anchor_id: str,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> StyleIngestResult:
        """Chunk, analyze with Groq, embed, and store a style source."""
        cleaned_text = normalize_text(text)

        if not style_anchor_id.strip():
            raise ValueError("style_anchor_id cannot be empty.")

        if not cleaned_text:
            raise ValueError("style source text cannot be empty.")

        chunks = chunk_text(
            cleaned_text,
            chunk_size_words=self.settings.chunk_size_words,
            overlap_words=self.settings.chunk_overlap_words,
        )

        telemetry = extract_linguistic_telemetry_with_groq(
            text=build_analysis_sample(chunks),
            extraction_llm=self.extraction_llm,
        )

        vectors = self.embedder.embed_texts(chunks)

        points = [
            build_style_point(
                style_anchor_id=style_anchor_id,
                chunk_text=chunk,
                chunk_index=index,
                vector=vector,
                telemetry=telemetry,
                metadata=metadata or {},
            )
            for index, (chunk, vector) in enumerate(zip(chunks, vectors, strict=True))
        ]

        self.qdrant_client.upsert(
            collection_name=self.settings.qdrant_collection,
            points=points,
        )

        return StyleIngestResult(
            style_anchor_id=style_anchor_id,
            chunks_stored=len(points),
            telemetry=telemetry,
            collection=self.settings.qdrant_collection,
        )


def extract_linguistic_telemetry_with_groq(
    text: str,
    extraction_llm: BaseChatModel,
) -> LinguisticTelemetry:
    """Use Groq to extract a validated linguistic telemetry object."""
    structured_llm = extraction_llm.with_structured_output(LinguisticTelemetry)

    result = structured_llm.invoke(
        [
            SystemMessage(content=STYLE_EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(
                content=STYLE_EXTRACTION_HUMAN_PROMPT.format(text=text),
            ),
        ]
    )

    if isinstance(result, LinguisticTelemetry):
        return result

    return LinguisticTelemetry.model_validate(result)


def build_style_point(
    style_anchor_id: str,
    chunk_text: str,
    chunk_index: int,
    vector: list[float],
    telemetry: LinguisticTelemetry,
    metadata: dict[str, Any],
) -> PointStruct:
    """Build one Qdrant point for a style chunk."""
    payload = StyleAnchorPayload(
        style_anchor_id=style_anchor_id,
        chunk_text=chunk_text,
        chunk_index=chunk_index,
        telemetry=telemetry,
        metadata=metadata,
    )

    point_id = str(uuid5(NAMESPACE_URL, f"style:{style_anchor_id}:{chunk_index}:{chunk_text}"))

    return PointStruct(
        id=point_id,
        vector=vector,
        payload=payload.to_qdrant_payload(),
    )


def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph breaks."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size_words: int, overlap_words: int) -> list[str]:
    """Split text into overlapping word chunks."""
    words = text.split()

    if not words:
        return []

    if chunk_size_words <= 0:
        raise ValueError("chunk_size_words must be greater than zero.")

    if overlap_words < 0:
        raise ValueError("chunk_overlap_words cannot be negative.")

    if overlap_words >= chunk_size_words:
        raise ValueError("chunk_overlap_words must be smaller than chunk_size_words.")

    chunks: list[str] = []
    step = chunk_size_words - overlap_words

    for start in range(0, len(words), step):
        chunk_words = words[start : start + chunk_size_words]
        if chunk_words:
            chunks.append(" ".join(chunk_words))

        if start + chunk_size_words >= len(words):
            break

    return chunks


def build_analysis_sample(chunks: list[str], max_chars: int = 12000) -> str:
    """Build a representative sample from the start, middle, and end chunks."""
    if not chunks:
        return ""

    selected_chunks = select_representative_chunks(chunks)
    sample = "\n\n".join(selected_chunks)

    if len(sample) <= max_chars:
        return sample

    return sample[:max_chars].rsplit(" ", 1)[0].strip()


def select_representative_chunks(chunks: list[str]) -> list[str]:
    """Select chunks that give the extractor a broad view of the source style."""
    if len(chunks) <= 3:
        return chunks

    middle_index = len(chunks) // 2
    return [
        chunks[0],
        chunks[middle_index],
        chunks[-1],
    ]