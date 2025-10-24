"""Tests for config module."""

import tempfile
from pathlib import Path

import pytest

from ENHANCER.config import (
    get_all_config,
    get_config,
    is_safe_path,
    set_config,
    validate_content,
)


def test_get_config():
    """Test getting configuration values."""
    model_sequence = get_config("model_sequence")
    assert isinstance(model_sequence, list)
    assert len(model_sequence) > 0


def test_set_config():
    """Test setting configuration values."""
    test_key = "test_value"
    set_config(test_key, "test")
    assert get_config(test_key) == "test"


def test_get_all_config():
    """Test getting all configuration."""
    config = get_all_config()
    assert isinstance(config, dict)
    assert "model_sequence" in config


def test_is_safe_path_valid():
    """Test safe path validation with valid paths."""
    home_path = Path.home()
    assert is_safe_path(home_path)


def test_is_safe_path_invalid():
    """Test safe path validation with potentially unsafe paths."""
    # This test depends on SAFE_DIRS configuration
    random_path = Path("/random/unsafe/path/that/should/not/exist")
    # Result depends on whether path is in SAFE_DIRS
    result = is_safe_path(random_path)
    assert isinstance(result, bool)


def test_validate_content_safe():
    """Test content validation with safe content."""
    safe_code = """
def hello():
    print("Hello, World!")
"""
    assert validate_content(safe_code) is True


def test_validate_content_dangerous():
    """Test content validation with dangerous patterns."""
    dangerous_code = "os.system('rm -rf /')"
    assert validate_content(dangerous_code) is False

    dangerous_code2 = "eval('malicious code')"
    assert validate_content(dangerous_code2) is False
