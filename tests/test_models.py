"""
Tests for models module.
"""

import pytest
from unittest.mock import Mock, patch

from ENHANCER.models import (
    ModelManager,
    get_model_manager,
    get_available_models,
    select_model,
    is_model_available,
    OLLAMA_MODELS,
    DEFAULT_MODEL_SEQUENCE,
)


class TestModelManager:
    """Tests for ModelManager class."""

    def test_init(self) -> None:
        """Test ModelManager initialization."""
        manager = ModelManager()
        assert hasattr(manager, 'ollama_available')
        assert hasattr(manager, 'available_ollama_models')
        assert hasattr(manager, 'api_keys')

    @patch('subprocess.run')
    def test_check_ollama_availability_success(self, mock_run: Mock) -> None:
        """Test successful Ollama detection."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="NAME\nmodel1:latest\nmodel2:latest\n"
        )

        manager = ModelManager()
        assert manager.ollama_available is True
        assert len(manager.available_ollama_models) > 0

    @patch('subprocess.run')
    def test_check_ollama_availability_failure(self, mock_run: Mock) -> None:
        """Test Ollama not available."""
        mock_run.side_effect = FileNotFoundError()

        manager = ModelManager()
        assert manager.ollama_available is False
        assert len(manager.available_ollama_models) == 0

    def test_get_available_models(self) -> None:
        """Test getting available models."""
        manager = ModelManager()
        models = manager.get_available_models()
        assert isinstance(models, dict)

    @patch.object(ModelManager, 'available_ollama_models', ['test-model:latest'])
    def test_select_model_with_preference(self) -> None:
        """Test selecting a specific model."""
        manager = ModelManager()
        manager.available_ollama_models = ['test-model:latest']

        model, provider = manager.select_model('test-model:latest')
        assert model == 'test-model:latest'
        assert provider == 'ollama'

    @patch.object(ModelManager, 'available_ollama_models', [])
    @patch.dict('os.environ', {}, clear=True)
    def test_select_model_no_models(self) -> None:
        """Test selecting model when none available."""
        manager = ModelManager()
        manager.available_ollama_models = []
        manager.api_keys = {}

        with pytest.raises(ValueError):
            manager.select_model()

    def test_is_model_available(self) -> None:
        """Test checking if model is available."""
        manager = ModelManager()
        manager.available_ollama_models = ['test-model:latest']

        assert manager.is_model_available('test-model:latest') is True
        assert manager.is_model_available('nonexistent:latest') is False

    def test_get_model_info_ollama(self) -> None:
        """Test getting model info for Ollama model."""
        manager = ModelManager()

        info = manager.get_model_info('codestral:latest')
        assert info is not None
        assert info.provider == 'ollama'
        assert info.requires_api_key is False

    def test_get_model_info_cloud(self) -> None:
        """Test getting model info for cloud model."""
        manager = ModelManager()

        info = manager.get_model_info('gpt-4')
        assert info is not None
        assert info.provider == 'openai'
        assert info.requires_api_key is True

    def test_get_model_info_unknown(self) -> None:
        """Test getting model info for unknown model."""
        manager = ModelManager()

        info = manager.get_model_info('unknown-model:latest')
        assert info is None


class TestModuleFunctions:
    """Tests for module-level convenience functions."""

    def test_get_model_manager_singleton(self) -> None:
        """Test that get_model_manager returns singleton."""
        manager1 = get_model_manager()
        manager2 = get_model_manager()
        assert manager1 is manager2

    def test_get_available_models_function(self) -> None:
        """Test get_available_models convenience function."""
        models = get_available_models()
        assert isinstance(models, dict)

    @patch.object(ModelManager, 'available_ollama_models', ['test:latest'])
    def test_is_model_available_function(self) -> None:
        """Test is_model_available convenience function."""
        # Reset singleton
        import ENHANCER.models
        ENHANCER.models._model_manager = None

        manager = get_model_manager()
        manager.available_ollama_models = ['test:latest']

        assert is_model_available('test:latest') is True
        assert is_model_available('nonexistent:latest') is False


class TestConstants:
    """Tests for module constants."""

    def test_ollama_models_list(self) -> None:
        """Test OLLAMA_MODELS constant."""
        assert isinstance(OLLAMA_MODELS, list)
        assert len(OLLAMA_MODELS) > 0
        assert 'codestral:latest' in OLLAMA_MODELS

    def test_default_model_sequence(self) -> None:
        """Test DEFAULT_MODEL_SEQUENCE constant."""
        assert isinstance(DEFAULT_MODEL_SEQUENCE, list)
        assert len(DEFAULT_MODEL_SEQUENCE) > 0
        assert DEFAULT_MODEL_SEQUENCE[0] == 'enhancer-llama:latest'
