"""Core code analysis functionality."""

import ast
from pathlib import Path
from typing import Dict, List, Optional, Union

from ENHANCER.config import MAX_FILE_SIZE, is_safe_path, validate_content
from ENHANCER.utils import format_file_size, setup_logging

logger = setup_logging(__name__)


class AnalysisResult:
    """Container for analysis results."""

    def __init__(
        self,
        file_path: Path,
        issues: List[Dict[str, Union[str, int]]],
        suggestions: List[str],
        metrics: Dict[str, Union[int, float]],
    ):
        self.file_path = file_path
        self.issues = issues
        self.suggestions = suggestions
        self.metrics = metrics

    def __repr__(self) -> str:
        return (
            f"AnalysisResult(file={self.file_path}, "
            f"issues={len(self.issues)}, "
            f"suggestions={len(self.suggestions)})"
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "file_path": str(self.file_path),
            "issues": self.issues,
            "suggestions": self.suggestions,
            "metrics": self.metrics,
        }


def is_valid_python_file(file_path: Path) -> bool:
    """Check if file is a valid Python file."""
    if not file_path.exists():
        return False

    if not file_path.is_file():
        return False

    if file_path.suffix != ".py":
        return False

    # Check file size
    try:
        size = file_path.stat().st_size
        if size > MAX_FILE_SIZE:
            logger.warning(
                f"File {file_path} is too large: {format_file_size(size)}"
            )
            return False
    except OSError as e:
        logger.error(f"Error checking file size: {e}")
        return False

    # Check if file is readable and has valid encoding
    try:
        with open(file_path, encoding="utf-8") as f:
            f.read(1)  # Try to read first character
        return True
    except (OSError, UnicodeDecodeError) as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return False


def validate_directory(directory: Path) -> None:
    """Validate directory exists and is accessible."""
    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    if not is_safe_path(directory):
        raise PermissionError(f"Directory is not in safe paths: {directory}")


def read_file_content(file_path: Path) -> str:
    """Read file content with error handling."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        if not validate_content(content):
            raise ValueError(f"File contains dangerous content: {file_path}")

        return content
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error reading {file_path}: {e}")
        raise
    except OSError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise


def analyze_syntax(code: str) -> List[Dict[str, Union[str, int]]]:
    """Analyze code for syntax errors."""
    issues = []

    try:
        ast.parse(code)
    except SyntaxError as e:
        issues.append({
            "type": "syntax_error",
            "message": str(e.msg),
            "line": e.lineno or 0,
            "severity": "critical",
        })

    return issues


def analyze_structure(code: str) -> Dict[str, Union[int, float]]:
    """Analyze code structure and complexity."""
    metrics: Dict[str, Union[int, float]] = {
        "lines": len(code.splitlines()),
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "complexity": 0,
    }

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics["functions"] += 1
            elif isinstance(node, ast.ClassDef):
                metrics["classes"] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics["imports"] += 1

        # Simple complexity estimate based on control flow statements
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                metrics["complexity"] += 1

    except SyntaxError:
        pass  # Already caught in analyze_syntax

    return metrics


def basic_code_analysis(code: str) -> List[Dict[str, Union[str, int]]]:
    """Perform basic static code analysis."""
    issues = []

    lines = code.splitlines()

    for i, line in enumerate(lines, start=1):
        # Check for common issues
        if len(line) > 120:
            issues.append({
                "type": "style",
                "message": "Line too long (>120 characters)",
                "line": i,
                "severity": "low",
            })

        if "TODO" in line or "FIXME" in line:
            issues.append({
                "type": "todo",
                "message": "TODO/FIXME comment found",
                "line": i,
                "severity": "info",
            })

        if "eval(" in line or "exec(" in line:
            issues.append({
                "type": "security",
                "message": "Dangerous function call detected",
                "line": i,
                "severity": "high",
            })

    return issues


def analyze_file(
    file_path: Path,
    auto_analyze: bool = True
) -> Optional[AnalysisResult]:
    """
    Analyze a Python file.

    Args:
        file_path: Path to the Python file
        auto_analyze: Whether to perform automatic analysis

    Returns:
        AnalysisResult object or None if analysis fails
    """
    if not isinstance(auto_analyze, bool):
        raise TypeError(f"auto_analyze must be bool, got {type(auto_analyze)}")

    if not is_safe_path(file_path):
        logger.error(f"File path not in safe directories: {file_path}")
        return None

    if not is_valid_python_file(file_path):
        logger.error(f"Invalid Python file: {file_path}")
        return None

    try:
        logger.info(f"Analyzing file: {file_path}")
        content = read_file_content(file_path)

        # Perform analysis
        issues = []
        suggestions = []

        # Syntax analysis
        syntax_issues = analyze_syntax(content)
        issues.extend(syntax_issues)

        # Structure analysis
        metrics = analyze_structure(content)

        # Basic code analysis
        if auto_analyze:
            basic_issues = basic_code_analysis(content)
            issues.extend(basic_issues)

            # Generate suggestions based on metrics
            if metrics["functions"] == 0 and metrics["classes"] == 0:
                suggestions.append(
                    "Consider organizing code into functions or classes"
                )

            if metrics["complexity"] > 20:
                suggestions.append(
                    "High complexity detected. Consider refactoring."
                )

        return AnalysisResult(
            file_path=file_path,
            issues=issues,
            suggestions=suggestions,
            metrics=metrics,
        )

    except Exception as e:
        logger.error(f"Error analyzing file {file_path}: {e}")
        return None


def analyze_directory(
    directory: Path,
    recursive: bool = True
) -> List[AnalysisResult]:
    """
    Analyze all Python files in a directory.

    Args:
        directory: Path to the directory
        recursive: Whether to analyze subdirectories

    Returns:
        List of AnalysisResult objects
    """
    validate_directory(directory)

    results = []
    pattern = "**/*.py" if recursive else "*.py"

    logger.info(f"Analyzing directory: {directory}")

    for file_path in directory.glob(pattern):
        if file_path.is_file():
            result = analyze_file(file_path)
            if result:
                results.append(result)

    logger.info(f"Analyzed {len(results)} files")
    return results


def get_critical_issues(results: List[AnalysisResult]) -> List[Dict]:
    """Extract critical issues from analysis results."""
    critical = []

    for result in results:
        for issue in result.issues:
            if issue.get("severity") in ["critical", "high"]:
                critical.append({
                    "file": str(result.file_path),
                    "issue": issue,
                })

    return critical
