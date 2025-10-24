"""Tests for code_analyzer module."""

import tempfile
from pathlib import Path

from ENHANCER.code_analyzer import (
    AnalysisResult,
    analyze_file,
    analyze_structure,
    analyze_syntax,
    basic_code_analysis,
    get_critical_issues,
    is_valid_python_file,
    read_file_content,
)


def test_analyze_syntax_valid():
    """Test syntax analysis with valid code."""
    valid_code = """
def hello():
    print("Hello")
"""
    issues = analyze_syntax(valid_code)
    assert len(issues) == 0


def test_analyze_syntax_invalid():
    """Test syntax analysis with invalid code."""
    invalid_code = "def hello(\n    pass"
    issues = analyze_syntax(invalid_code)
    assert len(issues) > 0
    assert issues[0]["type"] == "syntax_error"
    assert issues[0]["severity"] == "critical"


def test_analyze_structure():
    """Test code structure analysis."""
    code = """
import os
import sys

def function1():
    pass

def function2():
    pass

class MyClass:
    pass
"""
    metrics = analyze_structure(code)
    assert metrics["functions"] == 2
    assert metrics["classes"] == 1
    assert metrics["imports"] == 2
    assert metrics["lines"] > 0


def test_basic_code_analysis():
    """Test basic static analysis."""
    code = """
# TODO: Fix this
def long_line_function():
    x = "This is an extremely long line that exceeds the recommended maximum line length of 120 characters in Python PEP 8 style guide"
    eval("dangerous")
    return x
"""
    issues = basic_code_analysis(code)

    # Should find TODO comment
    todo_issues = [i for i in issues if i["type"] == "todo"]
    assert len(todo_issues) > 0

    # Should find eval usage
    security_issues = [i for i in issues if i["type"] == "security"]
    assert len(security_issues) > 0


def test_is_valid_python_file_valid():
    """Test Python file validation with valid file."""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write("print('hello')")
        f.flush()
        temp_path = Path(f.name)

    try:
        assert is_valid_python_file(temp_path) is True
    finally:
        temp_path.unlink()


def test_is_valid_python_file_not_python():
    """Test Python file validation with non-Python file."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"not python")
        temp_path = Path(f.name)

    try:
        assert is_valid_python_file(temp_path) is False
    finally:
        temp_path.unlink()


def test_is_valid_python_file_nonexistent():
    """Test Python file validation with nonexistent file."""
    fake_path = Path("/nonexistent/file.py")
    assert is_valid_python_file(fake_path) is False


def test_read_file_content():
    """Test file content reading."""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        test_content = "def test():\n    pass"
        f.write(test_content)
        f.flush()
        temp_path = Path(f.name)

    try:
        content = read_file_content(temp_path)
        assert content == test_content
    finally:
        temp_path.unlink()


def test_analyze_file():
    """Test full file analysis."""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write("def hello():\n    print('Hello')")
        f.flush()
        temp_path = Path(f.name)

    try:
        result = analyze_file(temp_path, auto_analyze=True)
        assert result is not None
        assert isinstance(result, AnalysisResult)
        assert result.file_path == temp_path
        assert isinstance(result.issues, list)
        assert isinstance(result.metrics, dict)
    finally:
        temp_path.unlink()


def test_analysis_result_to_dict():
    """Test AnalysisResult serialization."""
    result = AnalysisResult(
        file_path=Path("test.py"),
        issues=[{"type": "test", "message": "test"}],
        suggestions=["suggestion1"],
        metrics={"lines": 10}
    )

    result_dict = result.to_dict()
    assert "file_path" in result_dict
    assert "issues" in result_dict
    assert "suggestions" in result_dict
    assert "metrics" in result_dict


def test_get_critical_issues():
    """Test critical issue extraction."""
    results = [
        AnalysisResult(
            file_path=Path("test1.py"),
            issues=[
                {"type": "test", "severity": "critical", "message": "critical issue"},
                {"type": "test", "severity": "low", "message": "minor issue"}
            ],
            suggestions=[],
            metrics={}
        ),
        AnalysisResult(
            file_path=Path("test2.py"),
            issues=[
                {"type": "test", "severity": "high", "message": "high issue"}
            ],
            suggestions=[],
            metrics={}
        )
    ]

    critical = get_critical_issues(results)
    assert len(critical) == 2  # 1 critical + 1 high
    assert all(issue["issue"]["severity"] in ["critical", "high"] for issue in critical)
