"""Model definitions and management for ENHANCER."""

from typing import Dict, List

# Ollama models
OLLAMA_MODELS = [
    "enhancer-llama:latest",
    "codestral:latest",
    "qwen2.5-coder:latest",
    "deepseek-r1:latest",
    "phi4:latest",
    "command-r7b:latest",
    "llama3.2:latest",
    "llama3.3:latest",
    "olmo2:latest",
    "codellama:latest",
    "mistral:latest",
    "mixtral:latest",
    "gemma:latest",
    "gemma2:latest",
    "qwen:latest",
    "qwen2:latest",
    "deepseek-coder:latest",
    "codegemma:latest",
    "wizardcoder:latest",
    "phind-codellama:latest",
    "starcoder:latest",
    "neural-chat:latest",
    "solar:latest",
    "yi:latest",
    "orca-mini:latest",
    "vicuna:latest",
    "nous-hermes:latest",
    "dolphin-mixtral:latest",
    "openchat:latest",
    "starling-lm:latest",
]

# Cloud models
GROQ_MODELS = [
    "mixtral-8x7b-32768",
    "llama2-70b-4096",
    "llama3-70b-8192",
    "llama3-8b-8192",
]

OPENAI_MODELS = [
    "gpt-4",
    "gpt-4-turbo-preview",
    "gpt-3.5-turbo",
]

ANTHROPIC_MODELS = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-2.1",
]

GOOGLE_MODELS = [
    "gemini-pro",
    "gemini-pro-vision",
]

# Model categories
MODEL_PROVIDERS: Dict[str, List[str]] = {
    "ollama": OLLAMA_MODELS,
    "groq": GROQ_MODELS,
    "openai": OPENAI_MODELS,
    "anthropic": ANTHROPIC_MODELS,
    "google": GOOGLE_MODELS,
}


def get_all_models() -> List[str]:
    """Get list of all available models."""
    all_models = []
    for models in MODEL_PROVIDERS.values():
        all_models.extend(models)
    return all_models


def get_models_by_provider(provider: str) -> List[str]:
    """Get models for a specific provider."""
    return MODEL_PROVIDERS.get(provider.lower(), [])


def is_ollama_model(model: str) -> bool:
    """Check if model is an Ollama model."""
    return model in OLLAMA_MODELS


def get_provider_for_model(model: str) -> str:
    """Get provider name for a model."""
    for provider, models in MODEL_PROVIDERS.items():
        if model in models:
            return provider
    return "unknown"
