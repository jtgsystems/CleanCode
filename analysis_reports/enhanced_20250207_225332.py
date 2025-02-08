```python
"""
This script analyzes a given Python code file using the Groq API and provides recommendations for improvement.

Usage:
    python code_analyzer.py <code_file>

Example:
    python code_analyzer.py test_sample.py
"""

import sys
import requests
import json

def read_code_file(code_file):
    """
    Reads the contents of the given code file.

    Args:
        code_file (str): Path to the code file.

    Returns:
        str: Contents of the code file.
    """
    try:
        with open(code_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{code_file}' not found.")
        sys.exit(1)

def prepare_api_request(code):
    """
    Prepares the API request data.

    Args:
        code (str): Contents of the code file.

    Returns:
        dict: API request data.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert code analyzer. Focus on code quality, security, and best practices.",
            },
            {
                "role": "user",
                "content": f"""Analyze this code and provide specific recommendations for improvements:

```python
{code}
```

Format your response as:
ISSUES FOUND:
- [Category] Description of issue

RECOMMENDATIONS:
- Specific recommendation with example if applicable""",
            },
        ],
    }

    return url, headers, data

def send_api_request(url, headers, data):
    """
    Sends the API request and returns the response.

    Args:
        url (str): API URL.
        headers (dict): API request headers.
        data (dict): API request data.

    Returns:
        dict: API response.
    """
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def save_analysis_report(analysis):
    """
    Saves the analysis report to a file.

    Args:
        analysis (str): Analysis report.
    """
    with open("code_analysis_report.txt", "w") as f:
        f.write("CODE ANALYSIS REPORT\n")
        f.write("=" * 40 + "\n\n")
        f.write(analysis)

def main():
    if len(sys.argv) != 2:
        print("Usage: python code_analyzer.py <code_file>")
        sys.exit(1)

    code_file = sys.argv[1]
    print(f"Reading {code_file}...")
    sys.stdout.flush()

    code = read_code_file(code_file)
    url, headers, data = prepare_api_request(code)

    print("Sending request to Groq API...")
    sys.stdout.flush()

    response = send_api_request(url, headers, data)
    analysis = response["choices"][0]["message"]["content"]

    print("\nCODE ANALYSIS REPORT")
    print("=" * 40)
    print(analysis)
    sys.stdout.flush()

    save_analysis_report(analysis)
    print("\nAnalysis saved to: code_analysis_report.txt")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
```