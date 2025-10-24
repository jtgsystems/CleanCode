"""Utility functions for ENHANCER."""

import logging
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

from ENHANCER.config import (
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    MAX_RETRIES,
    RETRY_DELAY,
)

# Type variable for generic functions
T = TypeVar("T")


def setup_logging(name: str, log_file: Optional[Path] = None) -> logging.Logger:
    """Set up logging configuration."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file is None:
        log_file = LOG_FILE

    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except (OSError, PermissionError) as e:
        logger.warning(f"Could not create log file: {e}")

    return logger


def retry_on_failure(
    max_retries: int = MAX_RETRIES,
    delay: float = RETRY_DELAY,
    exceptions: tuple = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to retry function on failure."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
                        continue
                    raise

            # This should never be reached, but for type safety
            if last_exception:
                raise last_exception
            raise RuntimeError("Retry logic failed unexpectedly")

        return wrapper

    return decorator


def get_timestamp() -> str:
    """Get formatted timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    size: float = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def truncate_string(text: str, max_length: int = 1000) -> str:
    """Truncate string to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove dangerous characters."""
    dangerous_chars = ['/', '\\', '..', '\0', '\n', '\r']
    sanitized = filename
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '_')
    return sanitized


def is_valid_python_syntax(code: str) -> bool:
    """Check if code has valid Python syntax."""
    try:
        compile(code, '<string>', 'exec')
        return True
    except SyntaxError:
        return False


def count_lines(text: str) -> int:
    """Count lines in text."""
    return len(text.splitlines())


def extract_code_blocks(text: str) -> list[str]:
    """Extract code blocks from markdown-formatted text."""
    code_blocks: list[str] = []
    in_code_block = False
    current_block: list[str] = []

    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_code_block:
                code_blocks.append("\n".join(current_block))
                current_block = []
                in_code_block = False
            else:
                in_code_block = True
        elif in_code_block:
            current_block.append(line)

    return code_blocks
