"""
AI Model Configuration and Selection

Manages Ollama local models and cloud provider models (OpenAI, Anthropic, Google, Groq).
"""

import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

# Setup logging
logger = logging.getLogger(__name__)

# Ollama Models - 30+ supported models for code analysis
OLLAMA_MODELS: List[str] = [
    "enhancer-llama:latest",
    "codestral:latest",
    "qwen2.5-coder:latest",
    "deepseek-r1:latest",
    "phi4:latest",
    "command-r7b:latest",
    "llama3.2:latest",
    "llama3.3:latest",
    "olmo2:latest",
    "granite3.1-dense:latest",
    "granite3.1-moe:latest",
    "deepseek-coder:latest",
    "deepseek-coder-v2:latest",
    "codegemma:latest",
    "wizardcoder:latest",
    "starcoder2:latest",
    "mistral:latest",
    "mixtral:latest",
    "gemma2:latest",
    "qwen2.5:latest",
    "llama3.1:latest",
    "codellama:latest",
    "phi3:latest",
    "solar:latest",
    "orca-mini:latest",
    "vicuna:latest",
    "nous-hermes2:latest",
    "openhermes:latest",
    "dolphin-mixtral:latest",
    "falcon:latest",
]

# Default model fallback sequence
DEFAULT_MODEL_SEQUENCE: List[str] = [
    "enhancer-llama:latest",
    "codestral:latest",
    "qwen2.5-coder:latest",
    "deepseek-r1:latest",
    "phi4:latest",
    "command-r7b:latest",
    "llama3.2:latest",
    "olmo2:latest",
]

# Cloud provider configurations
CLOUD_PROVIDERS: Dict[str, List[str]] = {
    "groq": ["mixtral-8x7b-32768", "llama2-70b-4096", "llama3-70b-8192"],
    "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
    "anthropic": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-2.1"],
    "google": ["gemini-pro", "gemini-1.5-pro"],
}


@dataclass
class ModelConfig:
    """Configuration for an AI model."""
    name: str
    provider: str
    requires_api_key: bool
    recommended_for: List[str]
    max_tokens: Optional[int] = None
    timeout: int = 120


class ModelManager:
    """Manages AI model selection and availability checking."""

    def __init__(self):
        self.ollama_available: bool = False
        self.available_ollama_models: List[str] = []
        self.api_keys: Dict[str, Optional[str]] = {
            "groq": os.getenv("GROQ_API_KEY"),
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "google": os.getenv("GOOGLE_API_KEY"),
        }
        self._check_ollama_availability()

    def _check_ollama_availability(self) -> None:
        """Check if Ollama is available and list installed models."""
        try:
            import subprocess
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
            if result.returncode == 0:
                self.ollama_available = True
                # Parse ollama list output
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                self.available_ollama_models = [
                    line.split()[0] for line in lines if line.strip()
                ]
                logger.info(f"Ollama available with {len(self.available_ollama_models)} models")
            else:
                logger.warning("Ollama command failed")
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception) as e:
            logger.warning(f"Ollama not available: {e}")
            self.ollama_available = False

    def get_available_models(self) -> Dict[str, List[str]]:
        """Get all available models organized by provider."""
        available: Dict[str, List[str]] = {}

        # Add Ollama models
        if self.ollama_available and self.available_ollama_models:
            available["ollama"] = self.available_ollama_models

        # Add cloud providers with valid API keys
        for provider, models in CLOUD_PROVIDERS.items():
            if self.api_keys.get(provider):
                available[provider] = models

        return available

    def select_model(self, preferred_model: Optional[str] = None) -> tuple[str, str]:
        """
        Select an AI model for analysis.

        Args:
            preferred_model: User's preferred model name (optional)

        Returns:
            Tuple of (model_name, provider)

        Raises:
            ValueError: If no models are available
        """
        # If preferred model specified, try to use it
        if preferred_model:
            # Check Ollama
            if preferred_model in self.available_ollama_models:
                return (preferred_model, "ollama")

            # Check cloud providers
            for provider, models in CLOUD_PROVIDERS.items():
                if preferred_model in models and self.api_keys.get(provider):
                    return (preferred_model, provider)

            logger.warning(f"Preferred model '{preferred_model}' not available, using fallback")

        # Try default sequence
        for model in DEFAULT_MODEL_SEQUENCE:
            if model in self.available_ollama_models:
                logger.info(f"Selected model: {model} (ollama)")
                return (model, "ollama")

        # Try any available Ollama model
        if self.available_ollama_models:
            model = self.available_ollama_models[0]
            logger.info(f"Selected model: {model} (ollama)")
            return (model, "ollama")

        # Try cloud providers
        for provider, models in CLOUD_PROVIDERS.items():
            if self.api_keys.get(provider):
                model = models[0]
                logger.info(f"Selected model: {model} ({provider})")
                return (model, provider)

        raise ValueError(
            "No AI models available. Please install Ollama models or configure API keys."
        )

    def is_model_available(self, model_name: str) -> bool:
        """Check if a specific model is available."""
        if model_name in self.available_ollama_models:
            return True

        for provider, models in CLOUD_PROVIDERS.items():
            if model_name in models and self.api_keys.get(provider):
                return True

        return False

    def get_model_info(self, model_name: str) -> Optional[ModelConfig]:
        """Get configuration info for a model."""
        # Check Ollama
        if model_name in OLLAMA_MODELS:
            recommended = []
            if "coder" in model_name or "code" in model_name:
                recommended = ["code_analysis", "quality", "security"]
            elif "deepseek-r1" in model_name:
                recommended = ["reasoning", "complex_analysis"]
            elif "phi" in model_name or "command-r7b" in model_name:
                recommended = ["speed", "quick_analysis"]

            return ModelConfig(
                name=model_name,
                provider="ollama",
                requires_api_key=False,
                recommended_for=recommended,
                timeout=120
            )

        # Check cloud providers
        for provider, models in CLOUD_PROVIDERS.items():
            if model_name in models:
                max_tokens = 8000
                if "32768" in model_name or "8192" in model_name:
                    max_tokens = int(model_name.split("-")[-1])

                return ModelConfig(
                    name=model_name,
                    provider=provider,
                    requires_api_key=True,
                    recommended_for=["cloud", "high_quality"],
                    max_tokens=max_tokens,
                    timeout=60
                )

        return None


# Singleton instance
_model_manager: Optional[ModelManager] = None


def get_model_manager() -> ModelManager:
    """Get the singleton ModelManager instance."""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager


def get_available_models() -> Dict[str, List[str]]:
    """Get all available models (convenience function)."""
    return get_model_manager().get_available_models()


def select_model(preferred_model: Optional[str] = None) -> tuple[str, str]:
    """Select an AI model (convenience function)."""
    return get_model_manager().select_model(preferred_model)


def is_model_available(model_name: str) -> bool:
    """Check if model is available (convenience function)."""
    return get_model_manager().is_model_available(model_name)
