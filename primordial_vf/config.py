from __future__ import annotations

from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or .env."""

    model_config = SettingsConfigDict(
        extra="ignore",
    )

    qdrant_url: str = Field(alias="QDRANT_URL")
    qdrant_api_key: str = Field(alias="QDRANT_API_KEY")
    qdrant_collection: str = Field(default="vf_corpus", alias="QDRANT_COLLECTION")

    groq_api_key: str = Field(alias="GROQ_API_KEY")
    groq_generation_model: str = Field(
        default="llama-3.3-70b-versatile",
        alias="GROQ_GENERATION_MODEL",
    )
    groq_extraction_model: str = Field(
        default="llama-3.1-8b-instant",
        alias="GROQ_EXTRACTION_MODEL",
    )

    embedding_model: str = Field(
        default="nomic-ai/nomic-embed-text-v1.5",
        alias="EMBEDDING_MODEL",
    )
    embedding_dim: int = Field(default=768, alias="EMBEDDING_DIM")

    chunk_size_words: int = Field(default=450, alias="CHUNK_SIZE_WORDS")
    chunk_overlap_words: int = Field(default=75, alias="CHUNK_OVERLAP_WORDS")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()