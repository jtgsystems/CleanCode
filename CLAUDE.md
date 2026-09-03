# CLAUDE.md — Developer Reference Manual

This file provides comprehensive guidance for AI assistants, engineers, and contributors working on the **CleanCode** repository.

---

## 1. Project Overview

**CleanCode** is an enterprise-grade static and semantic code intelligence platform. It orchestrates local LLMs (via Ollama) and cloud reasoning APIs (Anthropic Claude, OpenAI, Groq, Google Gemini) to detect security vulnerabilities, logic defects, algorithmic bottlenecks, and architectural debt before code reaches production.

### Key Capabilities
- **Multi-Model AI Analysis**: Supports 30+ local Ollama models (Qwen 2.5 Coder, Codestral, DeepSeek-R1, Phi-4, Llama 3.3) plus leading cloud APIs.
- **Deep Code Quality Audits**: Detects CWE/OWASP vulnerabilities, code smells, complexity spikes, and best practice violations.
- **Automated AI Remediation**: Generates actionable code fixes and refactoring suggestions with side-by-side diff previews.
- **Multi-Interface Access**: Native Desktop GUI (`tkinter`), High-Throughput CLI (`enhancer`), and Real-Time VS Code Extension.
- **AST Pre-Filtering**: Instant AST parsing and syntax validation prior to LLM dispatch for maximum speed and token efficiency.

---

## 2. Core Architecture & Layout

```
CleanCode/
├── ENHANCER/                  # Primary Python package
│   ├── __init__.py            # Package initialization & exports
│   ├── cli.py                 # CLI interface implementation (argparse)
│   ├── gui.py                 # Tkinter GUI implementation (tabbed workbench)
│   ├── code_analyzer.py       # AST validation, metrics, issue extraction
│   ├── core.py                # Analysis orchestration, batching, timeouts
│   ├── models.py              # 30+ model configurations & cloud API clients
│   ├── analysis_reports/      # Exported report files (.txt, .json)
│   └── logs/                  # Application runtime logs
├── tests/                     # Test suite
│   ├── test_code_analyzer.py  # Unit tests for code analyzer & validation
│   └── test_models.py         # Unit tests for model selection & failover
├── vscode-extension/          # VS Code extension source
│   ├── src/                   # TypeScript extension code
│   │   ├── extension.ts       # Extension lifecycle entry point
│   │   ├── analyzer.ts        # Bridge to ENHANCER engine
│   │   ├── diagnostics.ts     # VS Code Problems panel reporter
│   │   ├── statusBar.ts       # Live metrics status bar item
│   │   └── providers/         # Tree view & diagnostic providers
│   ├── package.json           # Extension manifest & contribution points
│   └── tsconfig.json          # TypeScript build configuration
├── banner.png                 # Official repository header branding
├── setup.py                   # Setuptools packaging specification
├── pyproject.toml             # Build system & tool configurations
├── check_ollama.py            # Local Ollama GPU & connectivity diagnostic
├── test_analyzer.py           # Standalone validation script
├── README.md                  # Comprehensive user & developer documentation
├── AGENTS.md                  # SOTA 2026 Maintainer substrate policy
└── CLAUDE.md                  # This developer reference manual
```

---

## 3. Data Flow & Execution Pipeline

```
1. Input Source
   └── File / Directory / IDE Buffer
2. Preflight Validation (code_analyzer.py)
   ├── Path traversal sanitization (SAFE_DIRS check)
   ├── Encoding verification (UTF-8)
   └── Python AST syntax validation (ast.parse)
3. Model Routing & Dispatch (models.py + core.py)
   ├── Primary: Local Ollama (e.g., qwen2.5-coder, codestral, deepseek-r1)
   └── Fallback: Cloud API (Groq, Anthropic, OpenAI, Google)
4. Consensus & Analysis Execution
   ├── Issue classification (Security, Performance, Code Style, Bugs)
   └── Remediation patch generation (unified diff)
5. Surface Delivery
   ├── GUI: Side-by-side diff review & one-click apply
   ├── CLI: Formatted table & structured JSON/Markdown export
   └── VS Code: Inline diagnostics & quick-fix code actions
```

---

## 4. Development & Testing Commands

### Python Environment
```bash
# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Run full test suite with pytest
pytest tests/ -v

# Run standalone analyzer test script
python test_analyzer.py

# Check Ollama GPU & model status
python check_ollama.py

# Launch GUI workbench
enhancer-gui
# or
python -m ENHANCER.gui

# Execute CLI analysis
enhancer analyze path/to/file.py
enhancer analyze ./src --model qwen2.5-coder:latest
enhancer suggest path/to/file.py --output ./reports/
```

### VS Code Extension
```bash
cd vscode-extension

# Install npm dependencies
npm install

# Compile TypeScript
npm run compile

# Run TypeScript linter
npm run lint

# Package extension into .vsix
npm run package
```

---

## 5. Coding & Security Invariants

1. **Path Traversal Sandboxing**:
   - All file analysis operations must validate paths against safe root directories using `validate_directory()` and `is_safe_path()`.
   - Never resolve raw user input without canonicalization (`Path.resolve()`).
2. **Subprocess & Execution Safety**:
   - Never use `shell=True` when invoking external processes.
   - Always pass arguments as sanitized lists and set explicit execution timeouts.
3. **Fail-Closed Model Fallback**:
   - If a local model fails or times out, smoothly transition to the next configured fallback in `DEFAULT_MODEL_SEQUENCE`.
   - Return clear, diagnostic error messages rather than hanging or silently swallowing errors.
4. **Zero Made-To-Pass Tests**:
   - All tests in `tests/` must assert real observable behavior and be capable of failing on actual bugs.

---

## 6. JTG Systems Brand & Ownership

- **Author**: JTG Systems
- **Website**: [https://jtgsystems.com](https://jtgsystems.com)
- **Phone**: (905) 892-4555
- **Tips & Sponsorship**: `jtgsystems@gmail.com`
