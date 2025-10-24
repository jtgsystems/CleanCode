"""Analysis module with additional analysis functions."""

from pathlib import Path
from typing import Dict, List, Optional

from ENHANCER.ai_interface import analyze_code_with_ai
from ENHANCER.code_analyzer import analyze_file, read_file_content
from ENHANCER.utils import setup_logging

logger = setup_logging(__name__)


def full_analysis(
    file_path: Path,
    use_ai: bool = False,
    model: Optional[str] = None
) -> Dict:
    """
    Perform full analysis on a file.

    Args:
        file_path: Path to the file
        use_ai: Whether to use AI analysis
        model: AI model to use

    Returns:
        Dictionary with combined analysis results
    """
    logger.info(f"Starting full analysis: {file_path}")

    # Static analysis
    static_result = analyze_file(file_path, auto_analyze=True)

    if not static_result:
        logger.error("Static analysis failed")
        return {"error": "Static analysis failed"}

    result = {
        "file_path": str(file_path),
        "static_analysis": static_result.to_dict(),
    }

    # AI analysis if requested
    if use_ai:
        try:
            code = read_file_content(file_path)
            ai_result = analyze_code_with_ai(code, model)
            result["ai_analysis"] = ai_result
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            result["ai_analysis_error"] = str(e)

    return result


def compare_analyses(
    file_path: Path,
    models: List[str]
) -> Dict[str, object]:
    """
    Compare analysis results from multiple models.

    Args:
        file_path: Path to the file
        models: List of models to compare

    Returns:
        Dictionary with comparison results
    """
    logger.info(f"Comparing analyses for {file_path} with {len(models)} models")

    code = read_file_content(file_path)
    results: Dict[str, object] = {}

    for model in models:
        try:
            ai_result = analyze_code_with_ai(code, model)
            results[model] = ai_result
        except Exception as e:
            logger.error(f"Model {model} failed: {e}")
            results[model] = {"error": str(e)}

    return {
        "file_path": str(file_path),
        "model_results": results,
    }


def batch_analyze(
    file_paths: List[Path],
    use_ai: bool = False,
    model: Optional[str] = None
) -> List[Dict]:
    """
    Analyze multiple files.

    Args:
        file_paths: List of file paths
        use_ai: Whether to use AI analysis
        model: AI model to use

    Returns:
        List of analysis results
    """
    logger.info(f"Batch analyzing {len(file_paths)} files")

    results = []
    for file_path in file_paths:
        try:
            result = full_analysis(file_path, use_ai=use_ai, model=model)
            results.append(result)
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            results.append({
                "file_path": str(file_path),
                "error": str(e),
            })

    return results
