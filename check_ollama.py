"""Check Ollama GPU status."""

import json
import subprocess


def check_ollama_status():
    try:
        # Get Ollama version info
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        print("Ollama Models:")
        print(result.stdout)

        # Try to get GPU info
        nvidia_result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if nvidia_result.returncode == 0:
            print("\nGPU Info:")
            print(nvidia_result.stdout)
        else:
            print("\nNo NVIDIA GPU found or nvidia-smi not available")

    except subprocess.CalledProcessError as e:
        print(f"Error running Ollama command: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    check_ollama_status()
