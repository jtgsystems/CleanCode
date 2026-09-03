"""
Core Analysis Engine and Orchestration

Handles AI analysis execution, security checks, and result processing.
"""

import os
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from ENHANCER.code_analyzer import (
    is_valid_python_file,
    validate_encoding,
    validate_syntax,
    check_dangerous_patterns,
    get_file_metrics,
)
from ENHANCER.models import get_model_manager, select_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ENHANCER/logs/enhancer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Safe directories for analysis (security feature)
SAFE_DIRS: List[str] = [
    "/home/",
    "/tmp/",
    os.getcwd(),  # Current working directory
]

# Analysis timeout in seconds
ANALYSIS_TIMEOUT: int = 120

# Maximum file size for analysis (10 MB)
MAX_FILE_SIZE: int = 10 * 1024 * 1024


def validate_path_security(file_path: Path) -> bool:
    """
    Validate that a path is in a safe directory (prevents directory traversal).

    Args:
        file_path: Path to validate

    Returns:
        True if path is safe

    Raises:
        ValueError: If path is not in safe directories
    """
    resolved_path = file_path.resolve()

    # Check if path starts with any safe directory
    for safe_dir in SAFE_DIRS:
        safe_path = Path(safe_dir).resolve()
        try:
            resolved_path.relative_to(safe_path)
            return True
        except ValueError:
            continue

    raise ValueError(
        f"Path {file_path} is not in safe directories. "
        f"Safe directories: {SAFE_DIRS}"
    )


def analyze_with_ai(
    content: str,
    model_name: str,
    provider: str,
    analysis_type: str = "comprehensive"
) -> Dict[str, Any]:
    """
    Perform AI-powered code analysis.

    Args:
        content: Python code content
        model_name: Name of the AI model to use
        provider: Provider (ollama, openai, etc.)
        analysis_type: Type of analysis (comprehensive, quick, security)

    Returns:
        Analysis results from AI model
    """
    logger.info(f"Starting {analysis_type} analysis with {model_name} ({provider})")

    # Build analysis prompt based on type
    prompts = {
        "comprehensive": f"""Analyze this Python code comprehensively. Identify:
1. Code quality issues
2. Security vulnerabilities
3. Performance problems
4. Best practices violations
5. Potential bugs
6. Maintainability concerns

Code to analyze:
```python
{content}
```

Provide specific, actionable feedback with line numbers where applicable.""",

        "quick": f"""Quickly review this Python code for critical issues only:
```python
{content}
```

Focus on: security vulnerabilities, major bugs, and critical performance problems.""",

        "security": f"""Perform a security audit of this Python code:
```python
{content}
```

Identify: SQL injection, command injection, path traversal, unsafe deserialization,
hardcoded secrets, and other OWASP Top 10 vulnerabilities.""",

        "suggestions": f"""Suggest improvements for this Python code:
```python
{content}
```

Provide specific recommendations for: readability, efficiency, modern Python features,
and best practices. Include code examples.""",
    }

    prompt = prompts.get(analysis_type, prompts["comprehensive"])

    # Call AI model based on provider
    try:
        if provider == "ollama":
            result = _call_ollama(model_name, prompt)
        elif provider == "openai":
            result = _call_openai(model_name, prompt)
        elif provider == "anthropic":
            result = _call_anthropic(model_name, prompt)
        elif provider == "google":
            result = _call_google(model_name, prompt)
        elif provider == "groq":
            result = _call_groq(model_name, prompt)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        logger.info(f"Analysis completed successfully with {model_name}")
        return {
            "success": True,
            "model": model_name,
            "provider": provider,
            "analysis": result,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Analysis failed with {model_name}: {e}")
        return {
            "success": False,
            "model": model_name,
            "provider": provider,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def _call_ollama(model: str, prompt: str) -> str:
    """Call Ollama API for analysis."""
    try:
        import ollama
        response = ollama.generate(model=model, prompt=prompt)
        return response.get('response', '')
    except Exception as e:
        logger.error(f"Ollama API error: {e}")
        raise


def _call_openai(model: str, prompt: str) -> str:
    """Call OpenAI API for analysis."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise


def _call_anthropic(model: str, prompt: str) -> str:
    """Call Anthropic API for analysis."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Anthropic API error: {e}")
        raise


def _call_google(model: str, prompt: str) -> str:
    """Call Google Gemini API for analysis."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Google API error: {e}")
        raise


def _call_groq(model: str, prompt: str) -> str:
    """Call Groq API for analysis."""
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        raise


def perform_comprehensive_analysis(
    file_path: Path,
    model: Optional[str] = None,
    analysis_types: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Perform comprehensive analysis of a Python file.

    Args:
        file_path: Path to Python file
        model: Preferred AI model (optional)
        analysis_types: Types of analysis to perform

    Returns:
        Complete analysis results
    """
    start_time = time.time()

    # Security validation
    validate_path_security(file_path)

    # File validation
    if not is_valid_python_file(file_path):
        raise ValueError(f"Invalid Python file: {file_path}")

    # Check file size
    file_size = file_path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE} bytes)"
        )

    # Read and validate content
    try:
        content = file_path.read_text(encoding='utf-8')
        validate_encoding(file_path)
        validate_syntax(file_path, content)
    except Exception as e:
        raise ValueError(f"File validation failed: {e}")

    # Get file metrics
    metrics = get_file_metrics(file_path)

    # Check for dangerous patterns
    security_warnings = check_dangerous_patterns(content)

    # Select AI model
    try:
        selected_model, provider = select_model(model)
    except ValueError as e:
        logger.error(f"Model selection failed: {e}")
        # Return basic analysis without AI
        return {
            "file": str(file_path),
            "metrics": metrics,
            "security_warnings": security_warnings,
            "ai_analysis": {"error": str(e)},
            "execution_time": time.time() - start_time,
        }

    # Perform AI analyses
    if analysis_types is None:
        analysis_types = ["comprehensive", "security", "suggestions"]

    ai_results = {}
    for analysis_type in analysis_types:
        result = analyze_with_ai(content, selected_model, provider, analysis_type)
        ai_results[analysis_type] = result

    execution_time = time.time() - start_time

    return {
        "file": str(file_path),
        "metrics": metrics,
        "security_warnings": security_warnings,
        "ai_analysis": ai_results,
        "model_used": selected_model,
        "provider": provider,
        "execution_time": execution_time,
        "timestamp": datetime.now().isoformat(),
    }


def save_analysis_report(
    analysis_results: Dict[str, Any],
    report_type: str = "comprehensive"
) -> Path:
    """
    Save analysis results to a report file.

    Args:
        analysis_results: Results from analysis
        report_type: Type of report (comprehensive, critical, suggestions)

    Returns:
        Path to saved report
    """
    # Ensure report directory exists
    report_dir = Path("ENHANCER/analysis_reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report_type}_{timestamp}.json"
    report_path = report_dir / filename

    # Save as JSON
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)

    logger.info(f"Report saved to {report_path}")
    return report_path


def export_critical_issues(
    analysis_results: Dict[str, Any]
) -> Path:
    """
    Export only critical issues to a text file.

    Args:
        analysis_results: Results from analysis

    Returns:
        Path to exported file
    """
    report_dir = Path("ENHANCER/analysis_reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"critical_{timestamp}.txt"
    report_path = report_dir / filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"CRITICAL ISSUES REPORT\n")
        f.write(f"File: {analysis_results.get('file')}\n")
        f.write(f"Generated: {analysis_results.get('timestamp')}\n")
        f.write("=" * 80 + "\n\n")

        # Security warnings
        if analysis_results.get('security_warnings'):
            f.write("SECURITY WARNINGS:\n")
            for warning in analysis_results['security_warnings']:
                f.write(f"  - [{warning['severity'].upper()}] {warning['message']}\n")
            f.write("\n")

        # AI-detected issues
        if 'ai_analysis' in analysis_results:
            for analysis_type, result in analysis_results['ai_analysis'].items():
                if result.get('success'):
                    f.write(f"{analysis_type.upper()} ANALYSIS:\n")
                    f.write(result.get('analysis', 'No issues found.') + "\n\n")

    logger.info(f"Critical issues exported to {report_path}")
    return report_path
