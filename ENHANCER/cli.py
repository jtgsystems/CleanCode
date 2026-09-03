"""
Command-Line Interface for ENHANCER

Provides command-line access to code analysis functionality.
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, List

from ENHANCER.core import (
    perform_comprehensive_analysis,
    save_analysis_report,
    export_critical_issues,
)
from ENHANCER.code_analyzer import analyze_directory
from ENHANCER.models import get_available_models, select_model

# Configure logging for CLI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def cmd_analyze(args: argparse.Namespace) -> int:
    """
    Execute the analyze command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    path = Path(args.path)

    # Check if path exists
    if not path.exists():
        logger.error(f"Path does not exist: {path}")
        return 1

    # Determine if it's a file or directory
    if path.is_file():
        return _analyze_file(path, args)
    elif path.is_dir():
        return _analyze_directory(path, args)
    else:
        logger.error(f"Path is neither a file nor directory: {path}")
        return 1


def _analyze_file(file_path: Path, args: argparse.Namespace) -> int:
    """Analyze a single file."""
    try:
        logger.info(f"Analyzing file: {file_path}")

        # Perform analysis
        results = perform_comprehensive_analysis(
            file_path,
            model=args.model,
            analysis_types=args.types if hasattr(args, 'types') else None
        )

        # Display results
        print("\n" + "=" * 80)
        print(f"ANALYSIS RESULTS: {file_path}")
        print("=" * 80)

        # Show metrics
        if 'metrics' in results:
            print("\nFILE METRICS:")
            for key, value in results['metrics'].items():
                print(f"  {key}: {value}")

        # Show security warnings
        if results.get('security_warnings'):
            print("\nSECURITY WARNINGS:")
            for warning in results['security_warnings']:
                print(f"  [{warning['severity'].upper()}] {warning['message']}")

        # Show AI analysis
        if 'ai_analysis' in results:
            print("\nAI ANALYSIS:")
            for analysis_type, result in results['ai_analysis'].items():
                print(f"\n{analysis_type.upper()}:")
                if result.get('success'):
                    print(result.get('analysis', 'No analysis available'))
                else:
                    print(f"  Error: {result.get('error')}")

        print(f"\nExecution time: {results.get('execution_time', 0):.2f}s")
        print("=" * 80)

        # Save report if requested
        if args.save:
            report_path = save_analysis_report(results, "comprehensive")
            print(f"\nReport saved to: {report_path}")

        # Export critical issues if requested
        if args.export_critical:
            critical_path = export_critical_issues(results)
            print(f"Critical issues exported to: {critical_path}")

        return 0

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        return 1


def _analyze_directory(dir_path: Path, args: argparse.Namespace) -> int:
    """Analyze all Python files in a directory."""
    try:
        logger.info(f"Analyzing directory: {dir_path}")

        # Get directory analysis
        results = analyze_directory(
            dir_path,
            model=args.model,
            recursive=args.recursive,
        )

        # Display summary
        print("\n" + "=" * 80)
        print(f"DIRECTORY ANALYSIS: {dir_path}")
        print("=" * 80)
        print(f"Total files found: {results['total_files']}")
        print(f"Successfully analyzed: {results['successful']}")
        print(f"Failed: {results['failed']}")

        # Show errors if any
        if results['errors']:
            print("\nERRORS:")
            for error in results['errors']:
                print(f"  {error['file']}: {error['error']}")

        # Detailed analysis if requested
        if args.verbose:
            print("\nDETAILED RESULTS:")
            for file_result in results['files']:
                print(f"\n  File: {file_result['file']}")
                print(f"    Lines: {file_result.get('lines', 'N/A')}")
                print(f"    Size: {file_result.get('size', 'N/A')} bytes")
                if file_result.get('security_warnings'):
                    print(f"    Security warnings: {len(file_result['security_warnings'])}")

        print("=" * 80)

        # Save report if requested
        if args.save:
            report_path = save_analysis_report(results, "directory")
            print(f"\nReport saved to: {report_path}")

        return 0

    except Exception as e:
        logger.error(f"Directory analysis failed: {e}", exc_info=True)
        return 1


def cmd_suggest(args: argparse.Namespace) -> int:
    """
    Execute the suggest command to generate improvement suggestions.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code
    """
    path = Path(args.path)

    if not path.exists() or not path.is_file():
        logger.error(f"File not found: {path}")
        return 1

    try:
        logger.info(f"Generating suggestions for: {path}")

        results = perform_comprehensive_analysis(
            path,
            model=args.model,
            analysis_types=["suggestions"]
        )

        print("\n" + "=" * 80)
        print(f"IMPROVEMENT SUGGESTIONS: {path}")
        print("=" * 80)

        if 'ai_analysis' in results and 'suggestions' in results['ai_analysis']:
            suggestion_result = results['ai_analysis']['suggestions']
            if suggestion_result.get('success'):
                print(suggestion_result.get('analysis', 'No suggestions available'))
            else:
                print(f"Error: {suggestion_result.get('error')}")

        print("=" * 80)

        if args.save:
            report_path = save_analysis_report(results, "suggestions")
            print(f"\nSuggestions saved to: {report_path}")

        return 0

    except Exception as e:
        logger.error(f"Suggestion generation failed: {e}", exc_info=True)
        return 1


def cmd_models(args: argparse.Namespace) -> int:
    """
    List available AI models.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code
    """
    try:
        models = get_available_models()

        print("\n" + "=" * 80)
        print("AVAILABLE AI MODELS")
        print("=" * 80)

        if not models:
            print("No models available. Please install Ollama models or configure API keys.")
            return 1

        for provider, model_list in models.items():
            print(f"\n{provider.upper()}:")
            for model in model_list:
                print(f"  - {model}")

        print("\n" + "=" * 80)

        # Show selected model
        try:
            selected, provider = select_model(args.model if hasattr(args, 'model') else None)
            print(f"\nDefault selected model: {selected} ({provider})")
        except ValueError as e:
            logger.warning(f"Could not select model: {e}")

        return 0

    except Exception as e:
        logger.error(f"Failed to list models: {e}", exc_info=True)
        return 1


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="ENHANCER - Advanced Code Analysis & Enhancement Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global arguments
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Analyze command
    parser_analyze = subparsers.add_parser(
        'analyze',
        help='Analyze Python file or directory'
    )
    parser_analyze.add_argument(
        'path',
        type=str,
        help='Path to Python file or directory'
    )
    parser_analyze.add_argument(
        '--model', '-m',
        type=str,
        help='AI model to use for analysis'
    )
    parser_analyze.add_argument(
        '--recursive', '-r',
        action='store_true',
        default=True,
        help='Recursively analyze subdirectories (default: True)'
    )
    parser_analyze.add_argument(
        '--save', '-s',
        action='store_true',
        help='Save analysis report to file'
    )
    parser_analyze.add_argument(
        '--export-critical', '-e',
        action='store_true',
        help='Export critical issues to separate file'
    )

    # Suggest command
    parser_suggest = subparsers.add_parser(
        'suggest',
        help='Generate improvement suggestions for a file'
    )
    parser_suggest.add_argument(
        'path',
        type=str,
        help='Path to Python file'
    )
    parser_suggest.add_argument(
        '--model', '-m',
        type=str,
        help='AI model to use'
    )
    parser_suggest.add_argument(
        '--save', '-s',
        action='store_true',
        help='Save suggestions to file'
    )

    # Models command
    parser_models = subparsers.add_parser(
        'models',
        help='List available AI models'
    )
    parser_models.add_argument(
        '--model', '-m',
        type=str,
        help='Test specific model selection'
    )

    # Parse arguments
    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Execute command
    if args.command == 'analyze':
        return cmd_analyze(args)
    elif args.command == 'suggest':
        return cmd_suggest(args)
    elif args.command == 'models':
        return cmd_models(args)
    else:
        # If no command specified, show help
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
