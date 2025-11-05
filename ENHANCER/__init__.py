"""
ENHANCER - Advanced Code Analysis & Enhancement Tool

A comprehensive Python package for AI-powered code analysis using multiple
models from Ollama, OpenAI, Anthropic, Google, and Groq.

Main modules:
- core: Core analysis engine and orchestration
- code_analyzer: Code validation and analysis logic
- models: AI model configuration and selection
- cli: Command-line interface
- gui: Graphical user interface (Tkinter)
"""

__version__ = "1.0.0"
__author__ = "Roo"
__license__ = "MIT"

# Lazy imports to avoid circular dependencies
__all__ = [
    "analyze_file",
    "analyze_directory",
    "is_valid_python_file",
    "get_available_models",
    "select_model",
]


def __getattr__(name: str):
    """Lazy import for package-level exports."""
    if name == "analyze_file":
        from ENHANCER.code_analyzer import analyze_file
        return analyze_file
    elif name == "analyze_directory":
        from ENHANCER.code_analyzer import analyze_directory
        return analyze_directory
    elif name == "is_valid_python_file":
        from ENHANCER.code_analyzer import is_valid_python_file
        return is_valid_python_file
    elif name == "get_available_models":
        from ENHANCER.models import get_available_models
        return get_available_models
    elif name == "select_model":
        from ENHANCER.models import select_model
        return select_model
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
