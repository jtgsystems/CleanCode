#!/usr/bin/env python3
"""
CleanCode Standalone Smoke & AST Benchmark Runner (SOTA 2026)

Tests core analyzer functionality, file validation, security pattern scanning,
and measures AST parsing throughput in MB/s without external dependencies.
"""

import sys
import time
import tempfile
from pathlib import Path

from ENHANCER.code_analyzer import (
    analyze_file,
    analyze_directory,
    is_valid_python_file,
    validate_directory,
    calculate_ast_metrics,
    check_dangerous_patterns,
)


def run_smoke_tests() -> bool:
    print("=" * 65)
    print("🧪 CleanCode Standalone Smoke & Benchmark Suite")
    print("=" * 65)
    
    passed_count = 0
    total_count = 0

    def assert_test(name: str, condition: bool, note: str = "") -> None:
        nonlocal passed_count, total_count
        total_count += 1
        if condition:
            passed_count += 1
            print(f"  ✅ [PASS] {name:<42} {note}")
        else:
            print(f"  ❌ [FAIL] {name:<42} {note}")

    # 1. Invalid Extension Test
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=True) as f:
        f.write("print('not python file')\n")
        f.flush()
        assert_test("Invalid Extension Rejection", not is_valid_python_file(Path(f.name)))

    # 2. Corrupted UTF-8 Bytes Test
    with tempfile.NamedTemporaryFile(suffix=".py", mode="wb", delete=True) as f:
        f.write(b"\xff\xfe\x00\x00 invalid raw binary")
        f.flush()
        assert_test("Corrupted Encoding Rejection", not is_valid_python_file(Path(f.name)))

    # 3. Non-existent Directory Validation Test
    dir_exception_thrown = False
    try:
        validate_directory(Path("/tmp/nonexistent_clean_code_test_dir_xyz"))
    except FileNotFoundError:
        dir_exception_thrown = True
    assert_test("Missing Directory Trap", dir_exception_thrown)

    # 4. Dangerous Pattern & Shell Injection Detection
    sample_malicious_code = """
import os
import subprocess
import pickle

def unsafe_execution(user_input):
    os.system(f"rm -rf {user_input}")
    subprocess.Popen(f"ls {user_input}", shell=True)
    eval("2 + 2")
    pickle.loads(b"cos\\nsystem\\n(S'id'\\ntR.")
"""
    warnings = check_dangerous_patterns(sample_malicious_code)
    has_eval = any("eval" in w.get("message", "") for w in warnings)
    has_os_system = any("os.system" in w.get("message", "") for w in warnings)
    assert_test("Security Pattern Detector (CWE-78/95)", has_eval and has_os_system, f"Found {len(warnings)} security flags")

    # 5. AST Metrics & Cyclomatic Complexity
    sample_complex_code = """
def complex_algorithm(items):
    total = 0
    for x in items:
        if x > 10:
            total += x
        elif x > 5 and x <= 10:
            total += x * 2
        else:
            total -= 1
    return total
"""
    metrics = calculate_ast_metrics(sample_complex_code)
    complexity = metrics.get("cyclomatic_complexity", 0)
    assert_test("AST Cyclomatic Complexity", complexity >= 4, f"Complexity = {complexity}")

    # 6. High-Speed AST Parsing Benchmark
    iterations = 2000
    test_payload = sample_complex_code * 10
    payload_size_mb = (len(test_payload.encode('utf-8')) * iterations) / (1024 * 1024)

    start_t = time.perf_counter()
    for _ in range(iterations):
        calculate_ast_metrics(test_payload)
    duration_s = time.perf_counter() - start_t
    throughput_mb_s = payload_size_mb / max(0.0001, duration_s)

    assert_test("AST Engine Throughput", throughput_mb_s > 1.0, f"{throughput_mb_s:.2f} MB/s ({iterations} AST parses in {duration_s:.3f}s)")

    print("-" * 65)
    print(f"Results: {passed_count}/{total_count} assertions passed.")
    print("=" * 65)
    return passed_count == total_count


if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1)
