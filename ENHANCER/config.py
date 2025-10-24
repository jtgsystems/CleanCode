"""Configuration management for ENHANCER."""

import os
from pathlib import Path
from typing import Any, Dict

# Directories
BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent
ANALYSIS_REPORTS_DIR = BASE_DIR / "analysis_reports"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
ANALYSIS_REPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Safe directories for analysis (prevent path traversal)
SAFE_DIRS = [
    str(PROJECT_ROOT),
    "/tmp",
    str(Path.home()),
]

# API Keys from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Model configuration
DEFAULT_MODEL_SEQUENCE = [
    "enhancer-llama:latest",
    "codestral:latest",
    "qwen2.5-coder:latest",
    "deepseek-r1:latest",
    "phi4:latest",
    "command-r7b:latest",
    "llama3.2:latest",
    "olmo2:latest",
]

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# Analysis configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_RETRIES = 3
RETRY_DELAY = 2

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "enhancer.log"
GUI_LOG_FILE = LOGS_DIR / "enhancer_gui.log"

# Configuration store
_config: Dict[str, Any] = {
    "model_sequence": DEFAULT_MODEL_SEQUENCE.copy(),
    "ollama_host": OLLAMA_HOST,
    "ollama_timeout": OLLAMA_TIMEOUT,
    "max_retries": MAX_RETRIES,
    "retry_delay": RETRY_DELAY,
    "log_level": LOG_LEVEL,
}


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value."""
    return _config.get(key, default)


def set_config(key: str, value: Any) -> None:
    """Set configuration value."""
    _config[key] = value


def get_all_config() -> Dict[str, Any]:
    """Get all configuration values."""
    return _config.copy()


def is_safe_path(path: Path) -> bool:
    """Check if path is within safe directories."""
    try:
        resolved = path.resolve()
        return any(
            str(resolved).startswith(safe_dir)
            for safe_dir in SAFE_DIRS
        )
    except (OSError, RuntimeError):
        return False


def validate_content(content: str) -> bool:
    """Validate content for dangerous patterns."""
    dangerous_patterns = [
        "rm -rf",
        "sudo",
        "eval(",
        "exec(",
        "__import__",
        "compile(",
    ]

    content_lower = content.lower()
    return not any(pattern.lower() in content_lower for pattern in dangerous_patterns)
