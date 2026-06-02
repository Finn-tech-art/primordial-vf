from __future__ import annotations

from functools import lru_cache

from langchain_groq import ChatGroq

from primordial_vf.config import get_settings


@lru_cache
def get_extraction_llm() -> ChatGroq:
    """Return the Groq model used for style extraction."""
    settings = get_settings()

    return ChatGroq(
        model=settings.groq_extraction_model,
        temperature=0,
        api_key=settings.groq_api_key,
    )


@lru_cache
def get_generation_llm() -> ChatGroq:
    """Return the Groq model used for final text generation."""
    settings = get_settings()

    return ChatGroq(
        model=settings.groq_generation_model,
        temperature=0.5,
        api_key=settings.groq_api_key,
    )
