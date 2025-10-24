"""Tests for utils module."""

from pathlib import Path

import pytest

from ENHANCER.utils import (
    count_lines,
    extract_code_blocks,
    format_file_size,
    get_timestamp,
    is_valid_python_syntax,
    sanitize_filename,
    truncate_string,
)


def test_format_file_size():
    """Test file size formatting."""
    assert "1.00 KB" in format_file_size(1024)
    assert "1.00 MB" in format_file_size(1024 * 1024)
    assert "100.00 B" in format_file_size(100)


def test_get_timestamp():
    """Test timestamp generation."""
    timestamp = get_timestamp()
    assert isinstance(timestamp, str)
    assert len(timestamp) == 15  # Format: YYYYMMDD_HHMMSS


def test_truncate_string():
    """Test string truncation."""
    long_string = "a" * 2000
    truncated = truncate_string(long_string, max_length=100)
    assert len(truncated) <= 103  # 100 + "..."
    assert truncated.endswith("...")


def test_truncate_string_short():
    """Test that short strings are not truncated."""
    short_string = "hello"
    result = truncate_string(short_string, max_length=100)
    assert result == short_string


def test_sanitize_filename():
    """Test filename sanitization."""
    dangerous = "../../../etc/passwd"
    sanitized = sanitize_filename(dangerous)
    assert ".." not in sanitized
    assert "/" not in sanitized


def test_is_valid_python_syntax_valid():
    """Test Python syntax validation with valid code."""
    valid_code = "def hello():\n    pass"
    assert is_valid_python_syntax(valid_code) is True


def test_is_valid_python_syntax_invalid():
    """Test Python syntax validation with invalid code."""
    invalid_code = "def hello(\n    pass"
    assert is_valid_python_syntax(invalid_code) is False


def test_count_lines():
    """Test line counting."""
    text = "line1\nline2\nline3"
    assert count_lines(text) == 3


def test_extract_code_blocks():
    """Test code block extraction from markdown."""
    markdown = """
Some text
```python
code line 1
code line 2
```
More text
```
another block
```
"""
    blocks = extract_code_blocks(markdown)
    assert len(blocks) == 2
    assert "code line 1" in blocks[0]
    assert "another block" in blocks[1]


def test_extract_code_blocks_none():
    """Test code block extraction with no blocks."""
    markdown = "Just regular text"
    blocks = extract_code_blocks(markdown)
    assert len(blocks) == 0
