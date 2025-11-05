"""
Code Analysis and Validation Module

Handles Python file validation, syntax checking, encoding verification,
and directory analysis.
"""

import ast
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

# Dangerous patterns to detect in code
DANGEROUS_PATTERNS: List[str] = [
    "exec(",
    "eval(",
    "compile(",
    "__import__",
    "os.system(",
    "subprocess.Popen",
    "open(",  # Can be dangerous depending on context
]


def is_valid_python_file(file_path: Path) -> bool:
    """
    Validate that a file is a valid Python file.

    Args:
        file_path: Path to the file to validate

    Returns:
        True if file is a valid Python file, False otherwise
    """
    # Check extension
    if not str(file_path).endswith('.py'):
        logger.debug(f"File {file_path} is not a .py file")
        return False

    # Check if file exists
    if not file_path.exists():
        logger.debug(f"File {file_path} does not exist")
        return False

    # Check if it's a file (not directory)
    if not file_path.is_file():
        logger.debug(f"Path {file_path} is not a file")
        return False

    # Try to read and parse the file
    try:
        content = file_path.read_text(encoding='utf-8')
        # Try to parse as Python
        ast.parse(content)
        return True
    except UnicodeDecodeError:
        logger.debug(f"File {file_path} has encoding issues")
        return False
    except SyntaxError:
        logger.debug(f"File {file_path} has syntax errors")
        return False
    except Exception as e:
        logger.debug(f"File {file_path} validation failed: {e}")
        return False


def validate_encoding(file_path: Path) -> bool:
    """
    Validate that a file has valid UTF-8 encoding.

    Args:
        file_path: Path to the file to check

    Returns:
        True if encoding is valid, False otherwise

    Raises:
        UnicodeDecodeError: If file cannot be decoded as UTF-8
    """
    try:
        file_path.read_text(encoding='utf-8')
        return True
    except UnicodeDecodeError as e:
        logger.error(f"Invalid encoding in {file_path}: {e}")
        raise


def validate_syntax(file_path: Path, content: Optional[str] = None) -> bool:
    """
    Validate Python syntax of a file.

    Args:
        file_path: Path to the file
        content: Optional pre-loaded content

    Returns:
        True if syntax is valid, False otherwise

    Raises:
        SyntaxError: If Python syntax is invalid
    """
    try:
        if content is None:
            content = file_path.read_text(encoding='utf-8')
        ast.parse(content)
        return True
    except SyntaxError as e:
        logger.error(f"Syntax error in {file_path}: {e}")
        raise


def check_dangerous_patterns(content: str) -> List[Dict[str, Any]]:
    """
    Check for potentially dangerous code patterns.

    Args:
        content: Python code content to check

    Returns:
        List of warnings about dangerous patterns found
    """
    warnings: List[Dict[str, Any]] = []

    for pattern in DANGEROUS_PATTERNS:
        if pattern in content:
            warnings.append({
                "type": "security",
                "severity": "high",
                "pattern": pattern,
                "message": f"Potentially dangerous pattern detected: {pattern}",
            })

    return warnings


def validate_directory(directory: Path) -> bool:
    """
    Validate that a directory exists and is accessible.

    Args:
        directory: Path to the directory to validate

    Returns:
        True if directory is valid

    Raises:
        FileNotFoundError: If directory does not exist
        NotADirectoryError: If path is not a directory
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    return True


def find_python_files(directory: Path, recursive: bool = True) -> List[Path]:
    """
    Find all Python files in a directory.

    Args:
        directory: Directory to search
        recursive: Whether to search subdirectories

    Returns:
        List of Python file paths
    """
    validate_directory(directory)

    if recursive:
        return list(directory.rglob("*.py"))
    else:
        return list(directory.glob("*.py"))


def analyze_file(
    file_path: Path,
    model: Optional[str] = None,
    auto_analyze: bool = False
) -> Dict[str, Any]:
    """
    Analyze a Python file for issues and improvements.

    Args:
        file_path: Path to the Python file
        model: AI model to use (optional)
        auto_analyze: Whether to run analysis automatically

    Returns:
        Dictionary containing analysis results

    Raises:
        TypeError: If auto_analyze is not a boolean
        FileNotFoundError: If file does not exist
        ValueError: If file is not valid Python
    """
    # Type validation
    if not isinstance(auto_analyze, bool):
        raise TypeError(f"auto_analyze must be bool, got {type(auto_analyze).__name__}")

    # Validate file
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not is_valid_python_file(file_path):
        raise ValueError(f"Invalid Python file: {file_path}")

    # Read content with encoding validation
    try:
        content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid file encoding: {e}")

    # Validate syntax
    try:
        validate_syntax(file_path, content)
    except SyntaxError as e:
        raise ValueError(f"Python syntax error: {e}")

    # Check for dangerous patterns
    security_warnings = check_dangerous_patterns(content)

    # Basic analysis result
    result: Dict[str, Any] = {
        "file": str(file_path),
        "valid": True,
        "lines": len(content.splitlines()),
        "size": len(content),
        "security_warnings": security_warnings,
    }

    # If auto_analyze is True, would trigger AI analysis
    # (implementation in core.py)
    if auto_analyze:
        result["auto_analyzed"] = True
        logger.info(f"Auto-analysis requested for {file_path}")

    return result


def analyze_directory(
    directory: Path,
    model: Optional[str] = None,
    recursive: bool = True,
    auto_analyze: bool = False
) -> Dict[str, Any]:
    """
    Analyze all Python files in a directory.

    Args:
        directory: Directory to analyze
        model: AI model to use (optional)
        recursive: Whether to search subdirectories
        auto_analyze: Whether to run analysis automatically

    Returns:
        Dictionary containing analysis results for all files

    Raises:
        FileNotFoundError: If directory does not exist
        NotADirectoryError: If path is not a directory
    """
    validate_directory(directory)

    python_files = find_python_files(directory, recursive)
    logger.info(f"Found {len(python_files)} Python files in {directory}")

    results: Dict[str, Any] = {
        "directory": str(directory),
        "total_files": len(python_files),
        "files": [],
        "errors": [],
    }

    for file_path in python_files:
        try:
            file_result = analyze_file(file_path, model, auto_analyze)
            results["files"].append(file_result)
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            results["errors"].append({
                "file": str(file_path),
                "error": str(e),
            })

    results["successful"] = len(results["files"])
    results["failed"] = len(results["errors"])

    return results


def get_file_metrics(file_path: Path) -> Dict[str, Any]:
    """
    Get basic metrics about a Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        Dictionary with file metrics
    """
    content = file_path.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Count different types of lines
    code_lines = 0
    comment_lines = 0
    blank_lines = 0
    docstring_lines = 0

    in_docstring = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank_lines += 1
        elif stripped.startswith('#'):
            comment_lines += 1
        elif '"""' in stripped or "'''" in stripped:
            docstring_lines += 1
            in_docstring = not in_docstring
        elif in_docstring:
            docstring_lines += 1
        else:
            code_lines += 1

    return {
        "total_lines": len(lines),
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
        "docstring_lines": docstring_lines,
        "file_size": len(content),
    }
