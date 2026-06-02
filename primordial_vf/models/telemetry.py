from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


Register = Literal[
    "colloquial",
    "conversational",
    "neutral",
    "formal",
    "technical",
    "literary",
]

DominantMood = Literal[
    "declarative",
    "reflective",
    "interrogative",
    "imperative",
    "exclamatory",
    "mixed",
]

NarrativePerson = Literal[
    "first",
    "second",
    "third",
    "mixed",
    "unknown",
]


class LinguisticTelemetry(BaseModel):
    """Structured fingerprint of a writing style."""

    model_config = ConfigDict(extra="forbid")

    avg_sentence_len: float = Field(
        ge=0,
        description="Mean word count per sentence.",
    )
    sentence_len_variance: float = Field(
        ge=0,
        description="Variance in sentence length across the sample.",
    )
    short_sentence_ratio: float = Field(
        ge=0,
        le=1,
        description="Ratio of sentences shorter than 8 words.",
    )
    long_sentence_ratio: float = Field(
        ge=0,
        le=1,
        description="Ratio of sentences longer than 30 words.",
    )

    avg_paragraph_sentences: float = Field(
        ge=0,
        description="Mean number of sentences per paragraph.",
    )
    single_sentence_paragraph_ratio: float = Field(
        ge=0,
        le=1,
        description="Ratio of paragraphs containing only one sentence.",
    )

    comma_density: float = Field(
        ge=0,
        description="Commas per 100 words.",
    )
    em_dash_density: float = Field(
        ge=0,
        description="Em dashes per 100 words.",
    )
    semicolon_density: float = Field(
        ge=0,
        description="Semicolons per 100 words.",
    )
    colon_density: float = Field(
        ge=0,
        description="Colons per 100 words.",
    )
    question_density: float = Field(
        ge=0,
        description="Question marks per 100 words.",
    )
    exclamation_density: float = Field(
        ge=0,
        description="Exclamation marks per 100 words.",
    )

    contraction_density: float = Field(
        ge=0,
        description="Contractions per 100 words.",
    )
    first_person_density: float = Field(
        ge=0,
        description="First-person pronouns per 100 words.",
    )
    second_person_density: float = Field(
        ge=0,
        description="Second-person pronouns per 100 words.",
    )
    third_person_density: float = Field(
        ge=0,
        description="Third-person pronouns per 100 words.",
    )

    fragment_ratio: float = Field(
        ge=0,
        le=1,
        description="Estimated ratio of sentence fragments.",
    )

    register: Register = Field(
        description="Overall diction and formality level.",
    )
    dominant_mood: DominantMood = Field(
        description="Dominant sentence mood or rhetorical posture.",
    )
    narrative_person: NarrativePerson = Field(
        description="Dominant point of view used by the source text.",
    )

    rhetorical_devices: list[str] = Field(
        default_factory=list,
        description="Detected rhetorical devices, such as anaphora or parallelism.",
    )
    style_notes: list[str] = Field(
        default_factory=list,
        description="Short natural-language observations about the writing style.",
    )


class StyleAnchorPayload(BaseModel):
    """Qdrant payload for one stored style chunk."""

    model_config = ConfigDict(extra="forbid")

    source_type: Literal["style_anchor"] = "style_anchor"
    style_anchor_id: str = Field(min_length=1)
    chunk_text: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    telemetry: LinguisticTelemetry
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_qdrant_payload(self) -> dict[str, Any]:
        """Return a JSON-safe payload for Qdrant."""
        return self.model_dump(mode="json")