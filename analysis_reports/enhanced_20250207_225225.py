```python
import os
from typing import Dict, List
import requests
import logging

class CodeAnalyzer:
    """
    A class used to analyze code using different prompts.

    Attributes:
    ----------
    api_key : str
        The API key for the Groq API.
    url : str
        The URL for the Groq API.
    headers : Dict
        The headers for the API request.
    model : str
        The model used for analysis.
    """

    def __init__(self):
        """
        Initializes the CodeAnalyzer class.

        Raises:
        ------
        ValueError
            If the GROQ_API_KEY environment variable is not set.
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Using Mixtral model for both analyses but with different prompts
        self.model = "mixtral-8x7b-32768"

        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _analyze_with_prompt(self, code: str, prompt_type: str) -> Dict:
        """
        Analyze code using specified prompt type.

        Parameters:
        ----------
        code : str
            The code to analyze.
        prompt_type : str
            The type of prompt to use (quality or security).

        Returns:
        -------
        Dict
            A dictionary containing the analysis result.
        """
        system_messages = {
            "quality": "You are an expert code quality analyzer. Focus on code structure, readability, and best practices.",
            "security": "You are an expert security code reviewer. Focus on potential vulnerabilities, edge cases, and performance issues.",
        }

        prompt = f"""Analyze the following code focusing on {prompt_type} aspects.
        Provide specific, actionable recommendations for improvements.

        Code to analyze:
        ```python
        {code}
        ```

        Format your response as:
        ISSUES FOUND:
        - [Category] Description of issue

        RECOMMENDATIONS:
        - Specific recommendation with example if applicable"""

        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_messages[prompt_type]},
                        {"role": "user", "content": prompt},
                    ],
                },
            )
            response.raise_for_status()
            return {
                "type": prompt_type,
                "analysis": response.json()["choices"][0]["message"]["content"],
            }
        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}")
            return {"type": prompt_type, "error": str(e)}

    def analyze_code(self, code: str) -> Dict[str, List[Dict]]:
        """
        Analyze code using different prompts.

        Parameters:
        ----------
        code : str
            The code to analyze.

        Returns:
        -------
        Dict
            A dictionary containing the analysis results.
        """
        results = []
        for prompt_type in ["quality", "security"]:
            analysis = self._analyze_with_prompt(code, prompt_type)
            results.append(analysis)

        return {"analyses": results, "timestamp": os.path.getmtime(__file__)}

    def generate_report(self, analyses: Dict) -> str:
        """
        Generate a formatted report from the analyses.

        Parameters:
        ----------
        analyses : Dict
            A dictionary containing the analysis results.

        Returns:
        -------
        str
            A formatted report.
        """
        report = "CODE ANALYSIS REPORT\n" + "=" * 20 + "\n\n"

        for analysis in analyses["analyses"]:
            report += f"\nANALYSIS TYPE: {analysis['type'].upper()}\n"
            report += "-" * 40 + "\n"

            if "error" in analysis:
                report += f"Error during analysis: {analysis['error']}\n"
            else:
                report += f"{analysis['analysis']}\n"

            report += "\n" + "=" * 20 + "\n"

        return report


def main():
    # Example usage
    analyzer = CodeAnalyzer()
    code = "def add(a, b): return a + b"
    analyses = analyzer.analyze_code(code)
    report = analyzer.generate_report(analyses)
    print(report)


if __name__ == "__main__":
    main()
```