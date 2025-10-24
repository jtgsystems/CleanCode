"""AI model interface for code analysis and suggestions."""

from typing import Dict, List, Optional

from ENHANCER.config import (
    ANTHROPIC_API_KEY,
    DEFAULT_MODEL_SEQUENCE,
    GOOGLE_API_KEY,
    GROQ_API_KEY,
    OPENAI_API_KEY,
)
from ENHANCER.models import get_provider_for_model
from ENHANCER.utils import retry_on_failure, setup_logging

logger = setup_logging(__name__)


class AIInterface:
    """Interface for AI model interactions."""

    def __init__(self, model: Optional[str] = None):
        """Initialize AI interface with a model."""
        self.model = model or DEFAULT_MODEL_SEQUENCE[0]
        self.provider = get_provider_for_model(self.model)

    def query(self, prompt: str, context: Optional[str] = None) -> Optional[str]:
        """
        Query the AI model with a prompt.

        Args:
            prompt: The prompt to send to the model
            context: Optional context to include

        Returns:
            Model response or None if query fails
        """
        full_prompt = prompt
        if context:
            full_prompt = f"{context}\n\n{prompt}"

        try:
            if self.provider == "ollama":
                return self._query_ollama(full_prompt)
            if self.provider == "groq":
                return self._query_groq(full_prompt)
            if self.provider == "openai":
                return self._query_openai(full_prompt)
            if self.provider == "anthropic":
                return self._query_anthropic(full_prompt)
            if self.provider == "google":
                return self._query_google(full_prompt)
            logger.error(f"Unknown provider: {self.provider}")
            return None
        except Exception as e:
            logger.error(f"Error querying {self.model}: {e}")
            return None

    @retry_on_failure(max_retries=3)
    def _query_ollama(self, prompt: str) -> Optional[str]:
        """Query Ollama model."""
        try:
            import ollama

            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.get("message", {}).get("content")

        except ImportError:
            logger.error("ollama package not installed")
            return None
        except Exception as e:
            logger.error(f"Ollama query error: {e}")
            raise

    @retry_on_failure(max_retries=3)
    def _query_groq(self, prompt: str) -> Optional[str]:
        """Query Groq model."""
        if not GROQ_API_KEY:
            logger.error("GROQ_API_KEY not set")
            return None

        try:
            from groq import Groq

            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.choices[0].message.content

        except ImportError:
            logger.error("groq package not installed")
            return None
        except Exception as e:
            logger.error(f"Groq query error: {e}")
            raise

    @retry_on_failure(max_retries=3)
    def _query_openai(self, prompt: str) -> Optional[str]:
        """Query OpenAI model."""
        if not OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY not set")
            return None

        try:
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.choices[0].message.content

        except ImportError:
            logger.error("openai package not installed")
            return None
        except Exception as e:
            logger.error(f"OpenAI query error: {e}")
            raise

    @retry_on_failure(max_retries=3)
    def _query_anthropic(self, prompt: str) -> Optional[str]:
        """Query Anthropic Claude model."""
        if not ANTHROPIC_API_KEY:
            logger.error("ANTHROPIC_API_KEY not set")
            return None

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text

        except ImportError:
            logger.error("anthropic package not installed")
            return None
        except Exception as e:
            logger.error(f"Anthropic query error: {e}")
            raise

    @retry_on_failure(max_retries=3)
    def _query_google(self, prompt: str) -> Optional[str]:
        """Query Google Gemini model."""
        if not GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY not set")
            return None

        try:
            import google.generativeai as genai

            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)

            return response.text

        except ImportError:
            logger.error("google-generativeai package not installed")
            return None
        except Exception as e:
            logger.error(f"Google query error: {e}")
            raise


def analyze_code_with_ai(code: str, model: Optional[str] = None) -> Dict[str, List]:
    """
    Analyze code using AI model.

    Args:
        code: Code to analyze
        model: Model to use (uses default sequence if None)

    Returns:
        Dictionary with 'issues' and 'suggestions' lists
    """
    prompt = f"""Analyze the following Python code for:
1. Security vulnerabilities
2. Performance issues
3. Best practice violations
4. Potential bugs
5. Code quality issues

Provide a structured analysis with specific issues and line numbers where possible.

Code:
```python
{code}
```
"""

    models_to_try = [model] if model else DEFAULT_MODEL_SEQUENCE

    for model_name in models_to_try:
        try:
            logger.info(f"Trying model: {model_name}")
            ai = AIInterface(model_name)
            response = ai.query(prompt)

            if response:
                # Parse response (simplified - in production would need better parsing)
                return {
                    "issues": _parse_issues(response),
                    "suggestions": _parse_suggestions(response),
                }
        except Exception as e:
            logger.warning(f"Model {model_name} failed: {e}")
            continue

    logger.error("All models failed")
    return {"issues": [], "suggestions": []}


def generate_suggestions_with_ai(
    code: str,
    issues: List[Dict],
    model: Optional[str] = None
) -> List[str]:
    """
    Generate improvement suggestions using AI.

    Args:
        code: Original code
        issues: List of identified issues
        model: Model to use

    Returns:
        List of suggestions
    """
    issues_text = "\n".join(
        f"- {issue.get('type', 'unknown')}: {issue.get('message', 'N/A')}"
        for issue in issues
    )

    prompt = f"""Given the following code and identified issues, provide specific,
actionable suggestions for improvement:

Issues:
{issues_text}

Code:
```python
{code}
```

Provide numbered suggestions that are concrete and implementable.
"""

    models_to_try = [model] if model else DEFAULT_MODEL_SEQUENCE

    for model_name in models_to_try:
        try:
            ai = AIInterface(model_name)
            response = ai.query(prompt)

            if response:
                return _parse_suggestions(response)
        except Exception as e:
            logger.warning(f"Model {model_name} failed: {e}")
            continue

    return []


def _parse_issues(response: str) -> List[Dict]:
    """Parse issues from AI response."""
    issues = []

    lines = response.split("\n")
    for line in lines:
        line = line.strip()
        if any(keyword in line.lower() for keyword in ["issue", "problem", "error", "vulnerability"]):
            issues.append({
                "type": "ai_detected",
                "message": line,
                "severity": "medium",
            })

    return issues


def _parse_suggestions(response: str) -> List[str]:
    """Parse suggestions from AI response."""
    suggestions = []

    lines = response.split("\n")
    for line in lines:
        line = line.strip()
        # Look for numbered suggestions or bullet points
        if line and (line[0].isdigit() or line.startswith(("-", "*"))):
            # Remove numbering/bullets
            cleaned = line.lstrip("0123456789.-* ")
            if len(cleaned) > 10:  # Filter out short/empty lines
                suggestions.append(cleaned)

    return suggestions
