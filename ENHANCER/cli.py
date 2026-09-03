"""
Command-Line Interface for ENHANCER (SOTA 2026 Engine)

Provides high-throughput CLI subcommands for static AST analysis,
deep security auditing, AI-powered suggestion generation, environment diagnostics,
and model selection.
"""

import sys
import json
import time
import argparse
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from ENHANCER.core import (
    perform_comprehensive_analysis,
    save_analysis_report,
    export_critical_issues,
)
from ENHANCER.code_analyzer import (
    analyze_directory,
    analyze_file,
    calculate_ast_metrics,
    check_dangerous_patterns,
    get_file_metrics,
)
from ENHANCER.models import get_available_models, select_model, get_model_manager

# Configure logging for CLI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def cmd_analyze(args: argparse.Namespace) -> int:
    """Execute the analyze command on a file or directory."""
    path = Path(args.path)

    if not path.exists():
        logger.error(f"Path does not exist: {path}")
        return 1

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

        results = perform_comprehensive_analysis(
            file_path,
            model=args.model,
            analysis_types=args.types if hasattr(args, 'types') else None
        )

        if getattr(args, 'json', False):
            print(json.dumps(results, indent=2, default=str))
            return 0

        print("\n" + "=" * 80)
        print(f"ANALYSIS RESULTS: {file_path}")
        print("=" * 80)

        # Show metrics
        if 'metrics' in results:
            print("\nFILE METRICS:")
            for key, value in results['metrics'].items():
                if key != "functions":
                    print(f"  {key}: {value}")

        # Show security warnings
        if results.get('security_warnings'):
            print("\nSECURITY WARNINGS:")
            for warning in results['security_warnings']:
                sev = warning.get('severity', 'info').upper()
                msg = warning.get('message', '')
                line = f" (line {warning['line']})" if 'line' in warning else ""
                print(f"  [{sev}] {msg}{line}")

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

        if getattr(args, 'save', False):
            report_path = save_analysis_report(results, "comprehensive")
            print(f"\nReport saved to: {report_path}")

        if getattr(args, 'export_critical', False):
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

        results = analyze_directory(
            dir_path,
            model=args.model,
            recursive=args.recursive,
        )

        if getattr(args, 'json', False):
            print(json.dumps(results, indent=2, default=str))
            return 0

        print("\n" + "=" * 80)
        print(f"DIRECTORY ANALYSIS: {dir_path}")
        print("=" * 80)
        print(f"Total files found:      {results['total_files']}")
        print(f"Successfully analyzed:  {results['successful']}")
        print(f"Failed:                 {results['failed']}")

        if results['errors']:
            print("\nERRORS:")
            for error in results['errors']:
                print(f"  {error['file']}: {error['error']}")

        if getattr(args, 'verbose', False):
            print("\nDETAILED RESULTS:")
            for file_result in results['files']:
                print(f"\n  File: {file_result['file']}")
                print(f"    Lines: {file_result.get('lines', 'N/A')}")
                print(f"    Size:  {file_result.get('size', 'N/A')} bytes")
                if file_result.get('security_warnings'):
                    print(f"    Security warnings: {len(file_result['security_warnings'])}")

        print("=" * 80)

        if getattr(args, 'save', False):
            report_path = save_analysis_report(results, "directory")
            print(f"\nReport saved to: {report_path}")

        return 0

    except Exception as e:
        logger.error(f"Directory analysis failed: {e}", exc_info=True)
        return 1


def cmd_ast(args: argparse.Namespace) -> int:
    """Execute high-speed zero-LLM AST metrics & complexity inspection."""
    path = Path(args.path)
    if not path.exists() or not path.is_file():
        logger.error(f"File not found: {path}")
        return 1

    try:
        content = path.read_text(encoding='utf-8')
        start_t = time.perf_counter()
        metrics = calculate_ast_metrics(content)
        file_metrics = get_file_metrics(path)
        sec_warnings = check_dangerous_patterns(content) + metrics.get("ast_issues", [])
        duration_ms = (time.perf_counter() - start_t) * 1000

        report = {
            "file": str(path),
            "lines": file_metrics["total_lines"],
            "code_lines": file_metrics["code_lines"],
            "comment_lines": file_metrics["comment_lines"],
            "blank_lines": file_metrics["blank_lines"],
            "cyclomatic_complexity": metrics["cyclomatic_complexity"],
            "maintainability_index": metrics["maintainability_index"],
            "functions": metrics["functions"],
            "classes": metrics["class_count"],
            "imports": metrics["import_count"],
            "security_issues": sec_warnings,
            "latency_ms": round(duration_ms, 3),
        }

        if getattr(args, 'json', False):
            print(json.dumps(report, indent=2))
            return 0

        print("\n" + "=" * 80)
        print(f"⚡ AST METRICS & STRUCTURE AUDIT: {path}")
        print("=" * 80)
        print(f"Total Lines:              {report['lines']:<10} Code Lines:            {report['code_lines']}")
        print(f"Cyclomatic Complexity:    {report['cyclomatic_complexity']:<10} Maintainability Index: {report['maintainability_index']}/100")
        print(f"Functions:                {len(report['functions']):<10} Classes:               {report['classes']}")
        print(f"Imports:                  {report['imports']:<10} Scan Latency:          {report['latency_ms']} ms")

        if report["functions"]:
            print("\nFUNCTION COMPLEXITY MATRIX:")
            for f in report["functions"]:
                async_tag = "[async] " if f.get("is_async") else ""
                print(f"  • {async_tag}{f['name']:<32} Line {f['line']:<6} Complexity: {f['complexity']}")

        if report["security_issues"]:
            print("\nSECURITY & RELIABILITY WARNINGS:")
            for w in report["security_issues"]:
                sev = w.get("severity", "info").upper()
                msg = w.get("message", "")
                line = f" (line {w['line']})" if "line" in w else ""
                print(f"  [{sev}] {msg}{line}")
        else:
            print("\n✅ Zero static AST security issues detected.")

        print("=" * 80)
        return 0

    except Exception as e:
        logger.error(f"AST inspection failed: {e}", exc_info=True)
        return 1


def cmd_doctor(args: argparse.Namespace) -> int:
    """Check system environment, AI providers, and Ollama status."""
    manager = get_model_manager()
    available = manager.get_available_models()

    report: Dict[str, Any] = {
        "python_version": sys.version.split()[0],
        "ollama_available": manager.ollama_available,
        "available_ollama_models": manager.available_ollama_models,
        "cloud_providers_configured": list(manager.api_keys.keys()),
        "total_available_models": sum(len(m) for m in available.values()),
    }

    if getattr(args, 'json', False):
        print(json.dumps(report, indent=2))
        return 0

    print("=" * 80)
    print("🔱 CleanCode Environment & Provider Diagnostics (Doctor)")
    print("=" * 80)
    print(f"🐍 Python Runtime:           {report['python_version']}")
    print(f"🦙 Ollama Local Server:      {'ONLINE' if report['ollama_available'] else 'OFFLINE'}")
    print(f"📦 Local Ollama Models ({len(report['available_ollama_models'])}):  {', '.join(report['available_ollama_models']) if report['available_ollama_models'] else 'None detected'}")
    print(f"☁️  Configured Cloud APIs:     {', '.join(report['cloud_providers_configured']) if report['cloud_providers_configured'] else 'None (using local models only)'}")
    print(f"📊 Total Usable Models:       {report['total_available_models']}")
    print("=" * 80)
    return 0


def cmd_suggest(args: argparse.Namespace) -> int:
    """Generate improvement suggestions for a file."""
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

        if getattr(args, 'json', False):
            print(json.dumps(results, indent=2, default=str))
            return 0

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

        if getattr(args, 'save', False):
            report_path = save_analysis_report(results, "suggestions")
            print(f"\nSuggestions saved to: {report_path}")

        return 0

    except Exception as e:
        logger.error(f"Suggestion generation failed: {e}", exc_info=True)
        return 1


def cmd_models(args: argparse.Namespace) -> int:
    """List available AI models."""
    try:
        models = get_available_models()

        if getattr(args, 'json', False):
            print(json.dumps(models, indent=2))
            return 0

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
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="CleanCode - Advanced Multi-Model AI Code Analysis & Enhancement Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--json', action='store_true', help='Emit structured JSON output')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # 1. Analyze command
    parser_analyze = subparsers.add_parser('analyze', help='Analyze Python file or directory')
    parser_analyze.add_argument('path', type=str, help='Path to Python file or directory')
    parser_analyze.add_argument('--model', '-m', type=str, help='AI model to use for analysis')
    parser_analyze.add_argument('--recursive', '-r', action='store_true', default=True, help='Recursively analyze subdirectories')
    parser_analyze.add_argument('--save', '-s', action='store_true', help='Save analysis report to file')
    parser_analyze.add_argument('--export-critical', '-e', action='store_true', help='Export critical issues to file')
    parser_analyze.add_argument('--json', action='store_true', help='Emit structured JSON output')

    # 2. AST Command (Fast zero-LLM static check)
    parser_ast = subparsers.add_parser('ast', help='Instant static AST & complexity inspection (Zero LLM latency)')
    parser_ast.add_argument('path', type=str, help='Path to Python file')
    parser_ast.add_argument('--json', action='store_true', help='Emit structured JSON output')

    # 3. Suggest command
    parser_suggest = subparsers.add_parser('suggest', help='Generate improvement suggestions for a file')
    parser_suggest.add_argument('path', type=str, help='Path to Python file')
    parser_suggest.add_argument('--model', '-m', type=str, help='AI model to use')
    parser_suggest.add_argument('--save', '-s', action='store_true', help='Save suggestions to file')
    parser_suggest.add_argument('--json', action='store_true', help='Emit structured JSON output')

    # 4. Models command
    parser_models = subparsers.add_parser('models', help='List available AI models')
    parser_models.add_argument('--model', '-m', type=str, help='Test specific model selection')
    parser_models.add_argument('--json', action='store_true', help='Emit structured JSON output')

    # 5. Doctor command
    parser_doctor = subparsers.add_parser('doctor', help='Diagnostic check of local Ollama & cloud API providers')
    parser_doctor.add_argument('--json', action='store_true', help='Emit structured JSON output')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.command == 'analyze':
        return cmd_analyze(args)
    elif args.command == 'ast':
        return cmd_ast(args)
    elif args.command == 'suggest':
        return cmd_suggest(args)
    elif args.command == 'models':
        return cmd_models(args)
    elif args.command == 'doctor':
        return cmd_doctor(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
