"""
ENHANCER - Advanced Code Analysis & Enhancement Tool

A comprehensive Python-based tool that leverages multiple AI models
to analyze code for potential improvements, issues, and best practices.
"""

__version__ = "1.0.0"
__author__ = "Roo"

from ENHANCER.code_analyzer import analyze_directory, analyze_file
from ENHANCER.config import get_config, set_config

__all__ = [
    "analyze_file",
    "analyze_directory",
    "get_config",
    "set_config",
]
