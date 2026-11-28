"""
Code Analysis and Validation Module (SOTA 2026 Engine)

Handles Python file validation, syntax checking, encoding verification,
high-speed AST cyclomatic complexity calculation, security vulnerability
audits, and directory batch processing.
"""

import ast
import re
import math
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple

logger = logging.getLogger(__name__)

# Dangerous patterns to detect in code (regex / string matching)
DANGEROUS_PATTERNS: List[str] = [
    "exec(",
    "eval(",
    "compile(",
    "__import__",
    "os.system(",
    "subprocess.Popen",
    "open(",  # Can be dangerous depending on context
]

# Sensitive keys detection pattern
SECRET_KEY_REGEX = re.compile(
    r'(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token|password|bearer|aws[_-]?secret)\s*=\s*[\'"][^\'"\s]{8,}[\'"]'
)


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
    Check for potentially dangerous code patterns and security vulnerabilities.

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
                "severity": "high" if pattern in ["exec(", "eval(", "os.system("] else "medium",
                "pattern": pattern,
                "message": f"Potentially dangerous pattern detected: {pattern}",
            })

    # Check for hardcoded credentials / secrets
    for match in SECRET_KEY_REGEX.finditer(content):
        warnings.append({
            "type": "security",
            "severity": "critical",
            "pattern": "hardcoded_secret",
            "message": f"Possible hardcoded secret or API credential detected near: {match.group(0)[:25]}...",
        })

    return warnings


class ASTComplexityVisitor(ast.NodeVisitor):
    """AST visitor to compute cyclomatic complexity and code structure metrics."""

    def __init__(self) -> None:
        self.complexity: int = 1
        self.functions: List[Dict[str, Any]] = []
        self.classes: int = 0
        self.async_functions: int = 0
        self.imports: int = 0
        self.security_issues: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        func_visitor = ASTComplexityVisitor()
        for child in node.body:
            func_visitor.visit(child)
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "complexity": func_visitor.complexity,
            "is_async": False,
        })
        self.complexity += func_visitor.complexity - 1
        self._check_function_defaults(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.async_functions += 1
        func_visitor = ASTComplexityVisitor()
        for child in node.body:
            func_visitor.visit(child)
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "complexity": func_visitor.complexity,
            "is_async": True,
        })
        self.complexity += func_visitor.complexity - 1
        self._check_function_defaults(node)
        self.generic_visit(node)

    def _check_function_defaults(self, node: Any) -> None:
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.security_issues.append({
                    "type": "code_smell",
                    "severity": "medium",
                    "line": getattr(node, 'lineno', 0),
                    "message": f"Mutable default argument in function '{node.name}' (can cause shared state bugs)",
                })

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.classes += 1
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        self.imports += len(node.names)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.imports += len(node.names)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.complexity += 1
        if node.type is None:
            self.security_issues.append({
                "type": "reliability",
                "severity": "medium",
                "line": getattr(node, 'lineno', 0),
                "message": "Bare 'except:' clause caught — may swallow keyboard interrupts or critical exceptions",
            })
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Deep AST security checks for subprocess shell=True, eval, pickle, tempfile
        call_name = ""
        if isinstance(node.func, ast.Name):
            call_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            call_name = node.func.attr

        if call_name in ["Popen", "call", "run", "check_output", "check_call"]:
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.security_issues.append({
                        "type": "security",
                        "severity": "critical",
                        "line": getattr(node, 'lineno', 0),
                        "message": f"CWE-78: {call_name}() called with shell=True (remote code execution risk)",
                    })
        elif call_name == "mktemp":
            self.security_issues.append({
                "type": "security",
                "severity": "high",
                "line": getattr(node, 'lineno', 0),
                "message": "CWE-377: Insecure tempfile.mktemp() usage (race condition vulnerability)",
            })
        elif call_name == "loads" and any("pickle" in ast.dump(node) for _ in [1]):
            self.security_issues.append({
                "type": "security",
                "severity": "high",
                "line": getattr(node, 'lineno', 0),
                "message": "CWE-502: Deserialization of untrusted data via pickle.loads()",
            })

        self.generic_visit(node)


def calculate_ast_metrics(content: str) -> Dict[str, Any]:
    """
    Compute rich AST-based metrics, cyclomatic complexity, and maintainability index.

    Args:
        content: Python source code content

    Returns:
        Dictionary containing structural complexity analysis
    """
    try:
        tree = ast.parse(content)
        visitor = ASTComplexityVisitor()
        visitor.visit(tree)

        lines = content.splitlines()
        loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        
        # Calculate Halstead & Maintainability Index approximation
        volume = max(1.0, loc * math.log2(max(2.0, float(visitor.complexity + visitor.imports))))
        mi = max(0.0, min(100.0, 171.0 - 5.2 * math.log(volume) - 0.23 * visitor.complexity - 16.2 * math.log(max(1.0, float(loc)))))

        return {
            "cyclomatic_complexity": visitor.complexity,
            "maintainability_index": round(mi, 2),
            "function_count": len(visitor.functions),
            "async_function_count": visitor.async_functions,
            "class_count": visitor.classes,
            "import_count": visitor.imports,
            "functions": visitor.functions,
            "ast_issues": visitor.security_issues,
        }
    except Exception as e:
        logger.debug(f"AST metrics computation failed: {e}")
        return {
            "cyclomatic_complexity": 1,
            "maintainability_index": 50.0,
            "function_count": 0,
            "async_function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "functions": [],
            "ast_issues": [],
            "error": str(e),
        }


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
        return sorted(list(directory.rglob("*.py")))
    else:
        return sorted(list(directory.glob("*.py")))


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

    # Check for dangerous patterns & AST metrics
    security_warnings = check_dangerous_patterns(content)
    ast_metrics = calculate_ast_metrics(content)
    
    # Combine pattern warnings and AST security findings
    all_warnings = security_warnings + ast_metrics.get("ast_issues", [])

    # Basic analysis result
    result: Dict[str, Any] = {
        "file": str(file_path),
        "valid": True,
        "lines": len(content.splitlines()),
        "size": len(content),
        "security_warnings": all_warnings,
        "ast_metrics": ast_metrics,
    }

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
    Get comprehensive metrics about a Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        Dictionary with file metrics
    """
    content = file_path.read_text(encoding='utf-8')
    lines = content.splitlines()

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

    metrics: Dict[str, Any] = {
        "total_lines": len(lines),
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
        "docstring_lines": docstring_lines,
        "file_size": len(content),
    }

    # Attach AST metrics if parseable
    ast_info = calculate_ast_metrics(content)
    metrics["cyclomatic_complexity"] = ast_info.get("cyclomatic_complexity", 1)
    metrics["maintainability_index"] = ast_info.get("maintainability_index", 100.0)
    metrics["functions"] = ast_info.get("functions", [])
    metrics["classes"] = ast_info.get("class_count", 0)

    return metrics
