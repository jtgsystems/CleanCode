"""Enhancement pipeline module for code improvement processing."""

import ollama

from .config import Config
from .file_processor import FileProcessor


class EnhancementPipeline:
    """
    Implements the core enhancement logic with multiple processing phases.

    Each phase focuses on different aspects of code improvement, from structure
    and optimization to best practices and final polish.
    """

    def __init__(self):
        """Initialize the pipeline with model configurations."""
        self.models = Config.MODELS

    def enhance_phase(self, code, model_name, phase_prompt):
        """
        Enhances code using a specific model and phase-specific prompt.

        Args:
            code (str): The source code to enhance.
            model_name (str): Name of the model to use.
            phase_prompt (str): Phase-specific enhancement prompt.

        Returns:
            str: Enhanced code, or None if enhancement failed.
        """
        try:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{phase_prompt}\n\n"
                        "Current code:\n```\n"
                        f"{code}\n"
                        "```\n\n"
                        "Return ONLY the improved code without any "
                        "explanations or markdown."
                    ),
                }
            ]
            response = ollama.chat(model=model_name, messages=messages)
            improved_code = response["message"]["content"]

            # Clean up the response
            improved_code = improved_code.strip()
            if improved_code.startswith("```"):
                improved_code = improved_code.split("```")[1]
            if improved_code.startswith("python"):
                improved_code = improved_code[6:]
            improved_code = improved_code.strip()

            return improved_code
        except Exception as e:
            print(f"Error during code enhancement phase: {e}")
            return None

    def enhance_file(self, file_path):
        """
        Enhances a file through multiple phases of improvement.

        Args:
            file_path (str): Path of the file to enhance.

        Returns:
            str: Enhanced code, or None if enhancement failed.
        """
        try:
            current_code = FileProcessor.read_file(file_path)

            # Phase 1: Analysis and Structure
            analysis_prompt = """
            Analyze and improve this code focusing on:
            1. Code structure and organization
            2. Function decomposition
            3. Variable naming
            4. Code flow
            5. Documentation
            Make structural improvements while preserving functionality.
            """
            current_code = self.enhance_phase(
                current_code, self.models["analysis"], analysis_prompt
            )
            if not current_code:
                return None

            # Phase 2: Optimizations
            optimization_prompt = """
            Optimize this code focusing on:
            1. Algorithm efficiency
            2. Memory usage
            3. Time complexity
            4. Resource utilization
            5. Performance bottlenecks
            Implement optimizations while maintaining readability.
            """
            current_code = self.enhance_phase(
                current_code, self.models["generation"], optimization_prompt
            )
            if not current_code:
                return None

            # Phase 3: Best Practices
            review_prompt = """
            Review and improve this code focusing on:
            1. Best practices
            2. Design patterns
            3. SOLID principles
            4. DRY principle
            5. Code maintainability
            Apply industry standard practices while ensuring code quality.
            """
            current_code = self.enhance_phase(
                current_code, self.models["vetting"], review_prompt
            )
            if not current_code:
                return None

            # Phase 4: Error Handling
            implementation_prompt = """
            Enhance implementation focusing on:
            1. Error handling
            2. Edge cases
            3. Input validation
            4. Exception handling
            5. Defensive programming
            Implement robust error handling while maintaining code clarity.
            """
            current_code = self.enhance_phase(
                current_code, self.models["finalization"], implementation_prompt
            )
            if not current_code:
                return None

            # Phase 5: Advanced Optimization
            advanced_prompt = """
            Perform advanced optimization focusing on:
            1. Code elegance
            2. Functional programming concepts
            3. Modern language features
            4. Clean code principles
            5. Advanced patterns
            Apply sophisticated improvements while ensuring maintainability.
            """
            current_code = self.enhance_phase(
                current_code, self.models["enhancement"], advanced_prompt
            )
            if not current_code:
                return None

            # Phase 6: Comprehensive Review
            final_prompt = """
            Perform final review focusing on:
            1. Overall code quality
            2. Consistency
            3. Documentation completeness
            4. API design
            5. Future maintainability
            Ensure the code is perfect and production-ready.
            """
            current_code = self.enhance_phase(
                current_code, self.models["comprehensive"], final_prompt
            )
            if not current_code:
                return None

            # Phase 7: Final Polish
            polish_prompt = """
            Apply final polish focusing on:
            1. Code formatting
            2. Documentation style
            3. Comment clarity
            4. Naming consistency
            5. Overall aesthetics
            Ensure the code is pristine and professional and error free.
            """
            current_code = self.enhance_phase(
                current_code, self.models["presenter"], polish_prompt
            )
            if not current_code:
                return None

            return current_code
        except Exception as e:
            print(f"Error during code enhancement: {e}")
            return None
