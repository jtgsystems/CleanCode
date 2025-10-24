"""
Test cases for code analyzer.
"""

import tempfile
from pathlib import Path

from ENHANCER.code_analyzer import (
    analyze_file,
    is_valid_python_file,
    validate_directory,
)

# Test invalid Python file
with tempfile.NamedTemporaryFile(suffix=".txt") as f:
    f.write(b"not python code")
    f.flush()
    result = is_valid_python_file(Path(f.name))
    print(f"Invalid Python file test: {not result}")

# Test corrupted Python file
with tempfile.NamedTemporaryFile(suffix=".py") as f:
    f.write(b"\xff\xfe invalid bytes")
    f.flush()
    result = is_valid_python_file(Path(f.name))
    print(f"Corrupted Python file test: {not result}")

# Test non-existent directory
try:
    validate_directory(Path("nonexistent"))
    print("Directory validation failed")
except FileNotFoundError:
    print("Non-existent directory test: passed")

# Test invalid auto_analyze type
try:
    analyze_file(Path(__file__), auto_analyze="yes")
    print("auto_analyze validation failed")
except TypeError:
    print("Invalid auto_analyze type test: passed")

# Test file with invalid encoding
with tempfile.NamedTemporaryFile(suffix=".py") as f:
    f.write(b"\xff\xfe\xff\xfe")
    f.flush()
    try:
        analyze_file(Path(f.name), auto_analyze=True)
        print("Invalid encoding test failed")
    except Exception as e:
        print(f"Invalid encoding test: passed ({str(e)})")

print("All tests completed")
