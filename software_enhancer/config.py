"""Configuration module for the Software Enhancement Pipeline."""


class Config:
    """Configuration settings for models and progress messages."""

    MODELS = {
        # Project structure analysis
        "analysis": "llama3.2:latest",
        # Improvement suggestions
        "generation": "olmo2:13b",
        # Code review
        "vetting": "deepseek-r1",
        # Implementation planning
        "finalization": "deepseek-r1:14b",
        # Advanced optimization
        "enhancement": "phi4:latest",
        # Final project review
        "comprehensive": "phi4:latest",
        # Final report generation
        "presenter": "deepseek-r1:14b",
    }

    PROGRESS_MESSAGES = {
        "start": "Starting code enhancement pipeline...\n",
        "analyzing": (
            "Phase 1/7: Code Analysis - " "Understanding structure and patterns\n"
        ),
        "analysis_done": "Initial analysis complete.\n\n",
        "generating": (
            "Phase 2/7: Generating Improvements - "
            "Identifying optimization opportunities\n"
        ),
        "generation_done": "Improvement suggestions generated.\n\n",
        "vetting": ("Phase 3/7: Code Review - " "Validating proposed changes\n"),
        "vetting_done": "Code review complete.\n\n",
        "finalizing": (
            "Phase 4/7: Implementation - " "Applying validated improvements\n"
        ),
        "finalize_done": "Implementation complete.\n\n",
        "enhancing": ("Phase 5/7: Advanced Optimization - " "Fine-tuning the code\n"),
        "enhance_done": "Optimization complete.\n\n",
        "comprehensive": ("Phase 6/7: Final Review - " "Ensuring code perfection\n"),
        "comprehensive_done": "Final review complete.\n\n",
        "presenting": ("Phase 7/7: Final Polish - " "Applying finishing touches\n"),
        "complete": ("Enhancement pipeline complete. " "Code is now optimized.\n\n"),
    }
