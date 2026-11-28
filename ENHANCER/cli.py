"""Command-line interface for ENHANCER."""

import argparse
import sys
from pathlib import Path

from ENHANCER import __version__
from ENHANCER.ai_interface import analyze_code_with_ai, generate_suggestions_with_ai
from ENHANCER.code_analyzer import (
    analyze_directory,
    analyze_file,
    get_critical_issues,
)
from ENHANCER.models import get_all_models
from ENHANCER.utils import setup_logging

logger = setup_logging(__name__)


def print_banner() -> None:
    """Print application banner."""
    banner = f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  ENHANCER - Advanced Code Analysis & Enhancement Tool    ║
║  Version: {__version__:<48}║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def analyze_command(args: argparse.Namespace) -> int:
    """Execute analyze command."""
    path = Path(args.path).resolve()

    if not path.exists():
        logger.error(f"Path does not exist: {path}")
        return 1

    print(f"\n{'='*60}")
    print(f"Analyzing: {path}")
    print(f"{'='*60}\n")

    try:
        if path.is_file():
            result = analyze_file(path, auto_analyze=True)
            if result:
                results = [result]
            else:
                logger.error("Analysis failed")
                return 1
        else:
            results = analyze_directory(path, recursive=args.recursive)

        if not results:
            print("No Python files found to analyze.")
            return 0

        # Display results
        total_issues = sum(len(r.issues) for r in results)
        total_suggestions = sum(len(r.suggestions) for r in results)

        print("\nAnalysis Summary:")
        print(f"  Files analyzed: {len(results)}")
        print(f"  Total issues: {total_issues}")
        print(f"  Total suggestions: {total_suggestions}")

        # Show critical issues
        critical = get_critical_issues(results)
        if critical:
            print(f"\n{'='*60}")
            print("CRITICAL ISSUES:")
            print(f"{'='*60}")
            for item in critical[:10]:  # Show first 10
                print(f"\nFile: {item['file']}")
                print(f"  Type: {item['issue']['type']}")
                print(f"  Message: {item['issue']['message']}")
                print(f"  Line: {item['issue'].get('line', 'N/A')}")

        # Save report if requested
        if args.output:
            save_report(results, args.output)
            print(f"\nReport saved to: {args.output}")

        return 0

    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        return 1


def suggest_command(args: argparse.Namespace) -> int:
    """Execute suggest command."""
    path = Path(args.path).resolve()

    if not path.is_file():
        logger.error(f"Path must be a file: {path}")
        return 1

    print(f"\n{'='*60}")
    print(f"Generating suggestions for: {path}")
    print(f"{'='*60}\n")

    try:
        # Analyze file first
        result = analyze_file(path, auto_analyze=True)
        if not result:
            logger.error("Analysis failed")
            return 1

        # Read code
        with open(path, encoding="utf-8") as f:
            code = f.read()

        # Generate AI suggestions if model specified
        if args.model:
            print(f"Using AI model: {args.model}\n")
            suggestions = generate_suggestions_with_ai(
                code,
                result.issues,
                model=args.model
            )
        else:
            suggestions = result.suggestions

        if suggestions:
            print("Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"\n{i}. {suggestion}")
        else:
            print("No suggestions generated.")

        # Save suggestions if requested
        if args.output:
            save_suggestions(suggestions, args.output)
            print(f"\nSuggestions saved to: {args.output}")

        return 0

    except Exception as e:
        logger.error(f"Error generating suggestions: {e}")
        return 1


def enhance_command(args: argparse.Namespace) -> int:
    """Execute enhance command (AI-powered)."""
    path = Path(args.path).resolve()

    if not path.is_file():
        logger.error(f"Path must be a file: {path}")
        return 1

    print(f"\n{'='*60}")
    print(f"Enhancing: {path}")
    print(f"{'='*60}\n")

    try:
        # Read code
        with open(path, encoding="utf-8") as f:
            code = f.read()

        # Analyze with AI
        model = args.model
        print(f"Using AI model: {model or 'default'}\n")

        analysis = analyze_code_with_ai(code, model)

        print(f"Found {len(analysis['issues'])} issues")
        print(f"Generated {len(analysis['suggestions'])} suggestions")

        # Display
        if analysis['issues']:
            print("\nIssues:")
            for issue in analysis['issues'][:5]:
                print(f"  - {issue.get('message', 'N/A')}")

        if analysis['suggestions']:
            print("\nSuggestions:")
            for suggestion in analysis['suggestions'][:5]:
                print(f"  - {suggestion}")

        return 0

    except Exception as e:
        logger.error(f"Error during enhancement: {e}")
        return 1


def list_models_command(args: argparse.Namespace) -> int:
    """List available models."""
    print("\nAvailable Models:")
    print("=" * 60)

    models = get_all_models()
    for model in models:
        print(f"  - {model}")

    print(f"\nTotal: {len(models)} models")
    return 0


def save_report(results, output_path: Path) -> None:
    """Save analysis report to file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("ENHANCER Analysis Report\n")
        f.write("=" * 60 + "\n\n")

        for result in results:
            f.write(f"File: {result.file_path}\n")
            f.write(f"Metrics: {result.metrics}\n")
            f.write(f"Issues: {len(result.issues)}\n")

            for issue in result.issues:
                f.write(f"  - {issue}\n")

            f.write(f"Suggestions: {len(result.suggestions)}\n")
            for suggestion in result.suggestions:
                f.write(f"  - {suggestion}\n")

            f.write("\n" + "-" * 60 + "\n\n")


def save_suggestions(suggestions, output_path: Path) -> None:
    """Save suggestions to file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("ENHANCER Suggestions\n")
        f.write("=" * 60 + "\n\n")

        for i, suggestion in enumerate(suggestions, 1):
            f.write(f"{i}. {suggestion}\n\n")


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ENHANCER - Advanced Code Analysis & Enhancement Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"ENHANCER {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze Python code for issues"
    )
    analyze_parser.add_argument("path", help="File or directory to analyze")
    analyze_parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recursively analyze subdirectories"
    )
    analyze_parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Save report to file"
    )

    # Suggest command
    suggest_parser = subparsers.add_parser(
        "suggest",
        help="Generate improvement suggestions"
    )
    suggest_parser.add_argument("path", help="File to analyze")
    suggest_parser.add_argument(
        "-m", "--model",
        help="AI model to use for suggestions"
    )
    suggest_parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Save suggestions to file"
    )

    # Enhance command
    enhance_parser = subparsers.add_parser(
        "enhance",
        help="Analyze and enhance code with AI"
    )
    enhance_parser.add_argument("path", help="File to enhance")
    enhance_parser.add_argument(
        "-m", "--model",
        help="AI model to use"
    )

    # List models command
    subparsers.add_parser(
        "list-models",
        help="List available AI models"
    )

    args = parser.parse_args()

    # Print banner for non-list commands
    if args.command != "list-models":
        print_banner()

    # Execute command
    if args.command == "analyze":
        return analyze_command(args)
    if args.command == "suggest":
        return suggest_command(args)
    if args.command == "enhance":
        return enhance_command(args)
    if args.command == "list-models":
        return list_models_command(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
