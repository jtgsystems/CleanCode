# AGENTS.md — CleanCode Substrate Policy (SOTA 2026)

## 🔱 Senior Maintainer Contract & Universal Invariant

```text
FactionProductionReady(CleanCode) ⇔
  CorrectnessReady(S) ∧ SecurityReady(S) ∧ MultiModelConsensus(S) ∧
  TruthEvidenceReady(S) ∧ HonestTestingGate(S) ∧ FastASTPerformance(S)

CrossCuttingAxioms(CleanCode):
  ∀ defect: DiagnoseBeforeFix(defect)
  ∀ model_call: ValidateSchema(model_call) ∧ SecureFallback(model_call)
  ∀ file_op: PathTraversalSanitized(file_op) ∧ Sandboxed(file_op)
  ∀ test t: CanFail(t) ∧ AssertsObservableBehavior(t) ∧ ¬MADE_TO_PASS(t)
```

- **Default mode**: Smallest safe, verified change that solves the root problem.
- **Evidence-First**: Never report a task as complete, tested, or clean without attaching exact CLI outputs, test logs, or diff evidence.
- **Fail-Closed Security**: Never disable path validation (`SAFE_DIRS`), shell sanitization, or input encoding checks.

---

## 0. Truth, Evidence & Honest Testing Gate

`TRUTH_STATE_MACHINE = attempted ≠ succeeded ≠ verified ≠ committed ≠ pushed ≠ deployed ≠ live_verified`
`HONESTY ≻ GREEN_CI ≻ COVERAGE_%`
`MADE_TO_PASS(t) ⇔ ¬CanFail(t, claimed_behavior) ∨ ExpectedValueCopiedFromBuggyOutput(t) ∨ MockIsTheUnitUnderTest(t) ∨ FailureSwallowed(t)`
`TEST_GATE = Ship(test t) → CanFail(t) ∧ AssertsObservableBehavior(t) ∧ ¬MADE_TO_PASS(t)`

### Forbidden (Made-to-pass tests)
- `assert True`, `assert 1 == 1`, empty tests, or assertions on mocks instead of actual code behavior.
- Catching exceptions and silently passing to make tests go green.
- Modifying tests to match buggy output instead of fixing the root cause.
- Skipping failing tests (`@pytest.mark.skip`, `xit`) to mask defects.

### Required
1. Every test must test observable analyzer output (AST diagnostics, lint errors, model suggestions, exit codes).
2. Every test must have a plausible failing condition.
3. If an external model or live API is unreachable in CI, explicitly disclose the boundary—do not ship synthetic mock pass-throughs as acceptance proof.

---

## 1. Repository Snapshot & Architecture

- **Repository**: `jtgsystems/CleanCode`
- **Default Branch**: `master`
- **Visibility**: `public`
- **Tech Stack**:
  - **Core Engine**: Python 3.9+ (`setuptools`, `pyproject.toml`)
  - **Local AI Orchestration**: Ollama API (`ollama>=0.6.1`)
  - **Cloud AI Integrations**: Groq, Anthropic Claude, OpenAI, Google Gemini (`google-genai`)
  - **GUI Workbench**: Python `tkinter` (Standard Library)
  - **IDE Extension**: TypeScript / Node.js (`vscode-extension/`)

### Key Directories
```
CleanCode/
├── ENHANCER/                  # Primary Python package
│   ├── __init__.py            # Package initialization & exports
│   ├── cli.py                 # High-throughput CLI entry point (enhancer)
│   ├── gui.py                 # Native desktop GUI interface (enhancer-gui)
│   ├── code_analyzer.py       # AST parsing, file validation, metrics engine
│   ├── core.py                # Analysis orchestration, parallel batching, safety
│   ├── models.py              # 30+ Ollama & Cloud model registry & failover
│   ├── analysis_reports/      # Output directory for exported reports
│   └── logs/                  # Application runtime logs
├── tests/                     # Automated test suite
│   ├── test_code_analyzer.py  # Validation & AST parsing unit tests
│   └── test_models.py         # Model config & fallback unit tests
├── vscode-extension/          # Real-time VS Code LSP & Diagnostics Extension
│   ├── src/                   # Extension TypeScript sources
│   ├── package.json           # Extension manifests & commands
│   └── tsconfig.json          # TypeScript build config
├── banner.png                 # Official repository branding asset
├── setup.py                   # Python setuptools packaging
├── pyproject.toml             # Modern build system specifications
├── check_ollama.py            # Local Ollama GPU acceleration diagnostic
├── test_analyzer.py           # Quick standalone analyzer validation script
├── README.md                  # Comprehensive user & developer documentation
├── AGENTS.md                  # SOTA 2026 maintainer policy & invariants
└── CLAUDE.md                  # Architecture & developer reference manual
```

---

## 2. Command Map & Verification Standard

### Python Core & Analyzer
| Action | Command |
| :--- | :--- |
| **Install (Editable)** | `pip install -e ".[dev]"` |
| **Run Unit Tests** | `pytest tests/ -v` |
| **Quick Validation** | `python test_analyzer.py` |
| **Ollama Connectivity** | `python check_ollama.py` |
| **CLI Analyze File** | `enhancer analyze <file.py>` |
| **CLI Analyze Directory** | `enhancer analyze <dir> --model qwen2.5-coder:latest` |
| **CLI Suggest Improvements** | `enhancer suggest <file.py> --output ./reports/` |
| **Launch Desktop GUI** | `enhancer-gui` or `python -m ENHANCER.gui` |
| **Build Distribution** | `python -m build` |

### VS Code Extension
| Action | Command |
| :--- | :--- |
| **Install Dependencies** | `cd vscode-extension && npm install` |
| **Compile TypeScript** | `npm run compile` |
| **Lint Extension** | `npm run lint` |
| **Package VSIX** | `npm run package` |

---

## 3. Maintenance & Code Review Standards

1. **Security & Path Validation**:
   - Path operations must strictly enforce `SAFE_DIRS` restrictions in `core.py`.
   - Never allow directory traversal (`../`) to escape authorized workspaces.
   - Content analyzer must detect unsanitized `os.system`, `subprocess.Popen(..., shell=True)`, and exposed API keys.
2. **Multi-Model Consensus & Fallbacks**:
   - Model execution must support graceful fallback: `Local Ollama -> Secondary Ollama -> Cloud API (Groq/Claude/OpenAI)`.
   - Handle API timeouts and rate limits cleanly without hanging GUI or CLI execution.
3. **AST Speed & Memory Hygiene**:
   - Prefer AST-based static passes before invoking heavy LLM inference loops.
   - Stream large file reads and memoize repeated AST traversals.
4. **Git Rectification**:
   - Every landed change must be verified with test outputs and committed with a concise 1-3 sentence explanation.

---

*Authored for JTG Systems — Enterprise Systems Architecture & AI Solutions*
