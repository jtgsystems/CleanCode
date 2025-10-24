"""Tests for models module."""

import pytest

from ENHANCER.models import (
    get_all_models,
    get_models_by_provider,
    get_provider_for_model,
    is_ollama_model,
)


def test_get_all_models():
    """Test getting all models."""
    models = get_all_models()
    assert isinstance(models, list)
    assert len(models) > 0
    assert "codestral:latest" in models


def test_get_models_by_provider_ollama():
    """Test getting Ollama models."""
    ollama_models = get_models_by_provider("ollama")
    assert isinstance(ollama_models, list)
    assert len(ollama_models) > 0
    assert "codestral:latest" in ollama_models


def test_get_models_by_provider_groq():
    """Test getting Groq models."""
    groq_models = get_models_by_provider("groq")
    assert isinstance(groq_models, list)
    assert len(groq_models) > 0


def test_get_models_by_provider_invalid():
    """Test getting models for invalid provider."""
    models = get_models_by_provider("invalid_provider")
    assert models == []


def test_is_ollama_model():
    """Test Ollama model detection."""
    assert is_ollama_model("codestral:latest") is True
    assert is_ollama_model("gpt-4") is False


def test_get_provider_for_model_ollama():
    """Test provider detection for Ollama models."""
    provider = get_provider_for_model("codestral:latest")
    assert provider == "ollama"


def test_get_provider_for_model_openai():
    """Test provider detection for OpenAI models."""
    provider = get_provider_for_model("gpt-4")
    assert provider == "openai"


def test_get_provider_for_model_unknown():
    """Test provider detection for unknown models."""
    provider = get_provider_for_model("unknown-model-xyz")
    assert provider == "unknown"
