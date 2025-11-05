"""
Tests for code_analyzer module.
"""

import tempfile
import pytest
from pathlib import Path

from ENHANCER.code_analyzer import (
    is_valid_python_file,
    validate_encoding,
    validate_syntax,
    check_dangerous_patterns,
    validate_directory,
    find_python_files,
    analyze_file,
    analyze_directory,
    get_file_metrics,
)


class TestIsValidPythonFile:
    """Tests for is_valid_python_file function."""

    def test_valid_python_file(self, tmp_path: Path) -> None:
        """Test valid Python file passes validation."""
        file_path = tmp_path / "valid.py"
        file_path.write_text("print('hello')\n")
        assert is_valid_python_file(file_path) is True

    def test_invalid_extension(self, tmp_path: Path) -> None:
        """Test non-.py file fails validation."""
        file_path = tmp_path / "invalid.txt"
        file_path.write_text("print('hello')\n")
        assert is_valid_python_file(file_path) is False

    def test_nonexistent_file(self) -> None:
        """Test nonexistent file fails validation."""
        assert is_valid_python_file(Path("/nonexistent.py")) is False

    def test_corrupted_file(self, tmp_path: Path) -> None:
        """Test corrupted Python file fails validation."""
        file_path = tmp_path / "corrupted.py"
        file_path.write_bytes(b"\xff\xfe invalid bytes")
        assert is_valid_python_file(file_path) is False

    def test_syntax_error(self, tmp_path: Path) -> None:
        """Test Python file with syntax errors fails validation."""
        file_path = tmp_path / "syntax_error.py"
        file_path.write_text("def incomplete(\n")
        assert is_valid_python_file(file_path) is False


class TestValidateEncoding:
    """Tests for validate_encoding function."""

    def test_valid_utf8(self, tmp_path: Path) -> None:
        """Test valid UTF-8 encoded file."""
        file_path = tmp_path / "utf8.py"
        file_path.write_text("# -*- coding: utf-8 -*-\nprint('hello')\n")
        assert validate_encoding(file_path) is True

    def test_invalid_encoding(self, tmp_path: Path) -> None:
        """Test invalid encoding raises UnicodeDecodeError."""
        file_path = tmp_path / "invalid.py"
        file_path.write_bytes(b"\xff\xfe\xff\xfe")
        with pytest.raises(UnicodeDecodeError):
            validate_encoding(file_path)


class TestValidateSyntax:
    """Tests for validate_syntax function."""

    def test_valid_syntax(self, tmp_path: Path) -> None:
        """Test valid Python syntax."""
        file_path = tmp_path / "valid.py"
        file_path.write_text("def func():\n    return True\n")
        assert validate_syntax(file_path) is True

    def test_invalid_syntax(self, tmp_path: Path) -> None:
        """Test invalid Python syntax raises SyntaxError."""
        file_path = tmp_path / "invalid.py"
        file_path.write_text("def incomplete(\n")
        with pytest.raises(SyntaxError):
            validate_syntax(file_path)


class TestCheckDangerousPatterns:
    """Tests for check_dangerous_patterns function."""

    def test_safe_code(self) -> None:
        """Test safe code returns no warnings."""
        code = "def add(a, b):\n    return a + b\n"
        warnings = check_dangerous_patterns(code)
        assert len(warnings) == 0

    def test_exec_detected(self) -> None:
        """Test exec() is detected as dangerous."""
        code = "exec('malicious code')\n"
        warnings = check_dangerous_patterns(code)
        assert len(warnings) > 0
        assert any(w['pattern'] == 'exec(' for w in warnings)

    def test_eval_detected(self) -> None:
        """Test eval() is detected as dangerous."""
        code = "result = eval(user_input)\n"
        warnings = check_dangerous_patterns(code)
        assert len(warnings) > 0
        assert any(w['pattern'] == 'eval(' for w in warnings)

    def test_multiple_patterns(self) -> None:
        """Test multiple dangerous patterns detected."""
        code = "exec('code')\neval('expr')\n"
        warnings = check_dangerous_patterns(code)
        assert len(warnings) >= 2


class TestValidateDirectory:
    """Tests for validate_directory function."""

    def test_valid_directory(self, tmp_path: Path) -> None:
        """Test valid directory passes validation."""
        assert validate_directory(tmp_path) is True

    def test_nonexistent_directory(self) -> None:
        """Test nonexistent directory raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            validate_directory(Path("/nonexistent"))

    def test_file_instead_of_directory(self, tmp_path: Path) -> None:
        """Test file path raises NotADirectoryError."""
        file_path = tmp_path / "file.py"
        file_path.write_text("# test\n")
        with pytest.raises(NotADirectoryError):
            validate_directory(file_path)


class TestFindPythonFiles:
    """Tests for find_python_files function."""

    def test_find_python_files_recursive(self, tmp_path: Path) -> None:
        """Test finding Python files recursively."""
        (tmp_path / "file1.py").write_text("# test1\n")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file2.py").write_text("# test2\n")

        files = find_python_files(tmp_path, recursive=True)
        assert len(files) == 2

    def test_find_python_files_non_recursive(self, tmp_path: Path) -> None:
        """Test finding Python files non-recursively."""
        (tmp_path / "file1.py").write_text("# test1\n")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file2.py").write_text("# test2\n")

        files = find_python_files(tmp_path, recursive=False)
        assert len(files) == 1


class TestAnalyzeFile:
    """Tests for analyze_file function."""

    def test_analyze_valid_file(self, tmp_path: Path) -> None:
        """Test analyzing valid Python file."""
        file_path = tmp_path / "test.py"
        file_path.write_text("def func():\n    return True\n")

        result = analyze_file(file_path)
        assert result['valid'] is True
        assert 'lines' in result
        assert result['lines'] == 2

    def test_analyze_file_with_auto_analyze(self, tmp_path: Path) -> None:
        """Test auto_analyze parameter."""
        file_path = tmp_path / "test.py"
        file_path.write_text("def func():\n    return True\n")

        result = analyze_file(file_path, auto_analyze=True)
        assert result['auto_analyzed'] is True

    def test_invalid_auto_analyze_type(self, tmp_path: Path) -> None:
        """Test invalid auto_analyze type raises TypeError."""
        file_path = tmp_path / "test.py"
        file_path.write_text("def func():\n    return True\n")

        with pytest.raises(TypeError):
            analyze_file(file_path, auto_analyze="yes")

    def test_nonexistent_file(self) -> None:
        """Test analyzing nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            analyze_file(Path("/nonexistent.py"))

    def test_invalid_python_file(self, tmp_path: Path) -> None:
        """Test analyzing invalid Python file raises ValueError."""
        file_path = tmp_path / "invalid.txt"
        file_path.write_text("not python")

        with pytest.raises(ValueError):
            analyze_file(file_path)


class TestGetFileMetrics:
    """Tests for get_file_metrics function."""

    def test_basic_metrics(self, tmp_path: Path) -> None:
        """Test basic file metrics calculation."""
        file_path = tmp_path / "test.py"
        content = '''"""Docstring."""

def func():
    # Comment
    return True
'''
        file_path.write_text(content)

        metrics = get_file_metrics(file_path)
        assert 'total_lines' in metrics
        assert 'code_lines' in metrics
        assert 'comment_lines' in metrics
        assert 'blank_lines' in metrics
        assert 'docstring_lines' in metrics
        assert metrics['total_lines'] > 0
