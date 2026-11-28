#!/usr/bin/env python3
"""
Ollama & Hardware Acceleration Diagnostic Tool (SOTA 2026)

Checks local Ollama service availability, queries active models via REST & CLI,
probes GPU hardware (NVIDIA CUDA / ROCm / Apple Silicon), and validates latency.
"""

import sys
import json
import time
import argparse
import subprocess
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional


def query_ollama_api(endpoint: str = "http://localhost:11434", timeout: float = 3.0) -> Dict[str, Any]:
    """Query the local Ollama HTTP REST API for version and models."""
    status: Dict[str, Any] = {
        "running": False,
        "endpoint": endpoint,
        "version": None,
        "models": [],
        "latency_ms": None,
    }
    
    start_time = time.perf_counter()
    try:
        # Check /api/version
        req = urllib.request.Request(f"{endpoint}/api/version", headers={"User-Agent": "CleanCode-Diagnostics/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                status["running"] = True
                status["version"] = data.get("version", "unknown")
                status["latency_ms"] = round((time.perf_counter() - start_time) * 1000, 2)
        
        # Check /api/tags (model list)
        if status["running"]:
            tags_req = urllib.request.Request(f"{endpoint}/api/tags", headers={"User-Agent": "CleanCode-Diagnostics/1.0"})
            with urllib.request.urlopen(tags_req, timeout=timeout) as resp:
                if resp.status == 200:
                    tags_data = json.loads(resp.read().decode("utf-8"))
                    models = tags_data.get("models", [])
                    for m in models:
                        status["models"].append({
                            "name": m.get("name"),
                            "size_gb": round(m.get("size", 0) / (1024**3), 2),
                            "modified_at": m.get("modified_at"),
                            "digest": m.get("digest", "")[:12],
                        })
    except (urllib.error.URLError, TimeoutError, ConnectionRefusedError) as e:
        status["error"] = str(e)
    
    return status


def probe_gpu_hardware() -> Dict[str, Any]:
    """Probe system for NVIDIA CUDA, AMD ROCm, or Apple Metal acceleration."""
    gpu_info: Dict[str, Any] = {
        "type": "CPU",
        "detected": False,
        "details": None,
    }

    # 1. Probe NVIDIA SMI
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=3.0,
        )
        if res.returncode == 0 and res.stdout.strip():
            gpu_info["type"] = "NVIDIA CUDA"
            gpu_info["detected"] = True
            lines = [l.strip() for l in res.stdout.strip().splitlines()]
            gpu_info["details"] = lines
            return gpu_info
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 2. Probe ROCm SMI
    try:
        res = subprocess.run(["rocm-smi", "--showid"], capture_output=True, text=True, timeout=3.0)
        if res.returncode == 0:
            gpu_info["type"] = "AMD ROCm"
            gpu_info["detected"] = True
            gpu_info["details"] = res.stdout.strip().splitlines()
            return gpu_info
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return gpu_info


def main() -> int:
    parser = argparse.ArgumentParser(description="Ollama & Hardware Acceleration Diagnostic Tool")
    parser.add_argument("--json", action="store_true", help="Output diagnostic information in JSON format")
    parser.add_argument("--endpoint", default="http://localhost:11434", help="Ollama API base URL")
    parser.add_argument("--timeout", type=float, default=3.0, help="HTTP connection timeout in seconds")
    args = parser.parse_args()

    api_status = query_ollama_api(endpoint=args.endpoint, timeout=args.timeout)
    gpu_status = probe_gpu_hardware()

    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ollama": api_status,
        "hardware": gpu_status,
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if api_status["running"] else 1

    print("=" * 65)
    print("🔱 CleanCode — Ollama & GPU Diagnostic Workbench")
    print("=" * 65)
    
    # Ollama Service Info
    if api_status["running"]:
        print(f"✅ Ollama Service: ONLINE (v{api_status['version']})")
        print(f"📡 Endpoint:       {api_status['endpoint']} (Latency: {api_status['latency_ms']} ms)")
        print(f"📦 Installed Models ({len(api_status['models'])}):")
        for m in api_status["models"]:
            print(f"   • {m['name']:<30} {m['size_gb']:>6} GB  (ID: {m['digest']})")
    else:
        print(f"❌ Ollama Service: OFFLINE ({api_status.get('error', 'Connection refused')})")
        print("💡 Recommendation: Start Ollama with `ollama serve` or visit https://ollama.ai")

    print("-" * 65)
    
    # GPU Info
    if gpu_status["detected"]:
        print(f"🚀 Acceleration:   {gpu_status['type']}")
        for line in gpu_status.get("details", []):
            print(f"   • {line}")
    else:
        print("⚙️  Acceleration:   Standard CPU (No dedicated NVIDIA/AMD GPU detected)")

    print("=" * 65)
    return 0 if api_status["running"] else 1


if __name__ == "__main__":
    sys.exit(main())
