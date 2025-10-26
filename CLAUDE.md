# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

**CleanCode** is an advanced AI-powered code analysis and enhancement tool that leverages multiple AI models to analyze Python code for quality issues, security vulnerabilities, performance considerations, and best practices. The tool provides both a graphical user interface (GUI) and command-line capabilities for flexible usage.

**Key Features:**
- Multi-model AI analysis (30+ Ollama models + cloud providers)
- Comprehensive code quality assessment
- Security vulnerability detection
- Performance optimization suggestions
- Best practices adherence checking
- Interactive GUI with tabbed interface
- Export capabilities for reports and issues
- Parallel processing for batch analysis

## Core Architecture

### Package Structure

**ENHANCER Package** (primary module):
- Located in `ENHANCER/` directory
- Modular Python package with setuptools configuration
- Entry points for both CLI and GUI interfaces
- Installable via `pip install -e .` for development

**Key Components:**
- **Code Analyzer** (`code_analyzer.py`) — Core analysis engine
- **GUI Interface** (`gui.py`) — Tkinter-based graphical interface
- **CLI Interface** (`cli.py`) — Command-line interface
- **Model Manager** (`models.py`) — AI model configuration and selection
- **Core Engine** (`core.py`) — Analysis orchestration and execution

### Directory Structure

```
CleanCode/
├── ENHANCER/                  # Main package directory
│   ├── code_analyzer.py       # Code analysis logic
│   ├── gui.py                 # GUI implementation
│   ├── cli.py                 # Command-line interface
│   ├── models.py              # Model configuration
│   ├── core.py                # Core analysis engine
│   ├── analysis_reports/      # Generated analysis reports
│   └── logs/                  # Application logs
├── logs/                      # Root-level logs
│   └── debug.log              # Debug logging
├── .vscode/                   # VS Code configuration
│   └── settings.json          # Python linting settings
├── setup.py                   # Package configuration
├── test_analyzer.py           # Analyzer test suite
├── check_ollama.py            # Ollama GPU status checker
├── banner.png                 # Project banner
├── README.md                  # User documentation
├── .gitignore                 # Git ignore patterns
└── CLAUDE.md                  # This file
```

### Data Flow

1. **File Selection** → User selects Python file(s) or directory via GUI/CLI
2. **Validation** → Path validation, Python syntax check, encoding validation
3. **Model Selection** → Choose from Ollama local models or cloud providers
4. **Analysis** → AI model analyzes code for issues, vulnerabilities, best practices
5. **Report Generation** → Results formatted and displayed/exported
6. **Enhancement** → Optional AI-suggested improvements
7. **Export** → Save reports to `analysis_reports/` directory

## Technology Stack

### Core Dependencies

**Python 3.8+** (minimum version):
- **tkinter** — GUI framework (standard library)
- **requests** (≥2.25.0) — HTTP client
- **python-dotenv** (≥0.19.0) — Environment variable management
- **ollama** (≥0.1.0) — Local model interface

**AI Provider Libraries:**
- **groq** (≥0.3.0) — Groq API client
- **openai** (≥1.0.0) — OpenAI API client
- **anthropic** (≥0.5.0) — Claude API client
- **google-generativeai** (≥0.1.0) — Google Gemini API client
- **tiktoken** (≥0.5.0) — Token counting for OpenAI models

### Development Tools

**Linting Configuration (.vscode/settings.json):**
- **Flake8**: Ignores E501 (line too long), max line length 999999
- **Pylint**: Max line length 999999
- Purpose: Allow long lines for AI-generated code and complex expressions

**Version Control:**
- Git repository with GitHub remote
- Main branch: `master`
- Remote: `git@github.com:jtgsystems/CleanCode.git`

## Development Commands

### Installation & Setup

```bash
# Clone repository
git clone git@github.com:jtgsystems/CleanCode.git
cd CleanCode

# Install in development mode (creates 'enhancer' command globally)
pip install -e .

# Verify installation
enhancer --version  # Should launch GUI or show version

# Check Ollama status and GPU
python check_ollama.py
```

### Running the Application

```bash
# Launch GUI (primary interface)
enhancer

# Alternative: Run GUI directly
python -m ENHANCER.gui

# Command-line analysis of a file
python -m ENHANCER.cli analyze path/to/file.py

# Analyze directory
python -m ENHANCER.cli analyze path/to/directory

# Generate suggestions for a file
python -m ENHANCER.cli suggest path/to/file.py

# Specify a model
python -m ENHANCER.cli analyze path/to/file.py --model codestral:latest
```

### Testing

```bash
# Run analyzer test suite
python test_analyzer.py

# Expected output:
# - Invalid Python file test: True
# - Corrupted Python file test: True
# - Non-existent directory test: passed
# - Invalid auto_analyze type test: passed
# - Invalid encoding test: passed
# - All tests completed
```

### Ollama Management

```bash
# Check Ollama models and GPU status
python check_ollama.py

# List installed Ollama models
ollama list

# Install a new model
ollama pull codestral:latest
ollama pull qwen2.5-coder:latest

# Start Ollama server (if not running)
ollama serve
```

## AI Model Configuration

### Supported Model Categories

**Local Ollama Models (30+ supported):**
- **enhancer-llama:latest** — Custom model optimized for code analysis
- **codestral:latest** — Mistral's code-specialized model
- **qwen2.5-coder:latest** — Alibaba's coding model
- **deepseek-r1:latest** — DeepSeek reasoning model
- **phi4:latest** — Microsoft's compact model
- **command-r7b:latest** — Cohere command model
- **llama3.2:latest**, **llama3.3:latest** — Meta's Llama models
- **olmo2:latest** — AI2's open model
- And 20+ more (see README.md for complete list)

**Cloud Provider Models (optional, requires API keys):**
- **Groq**: mixtral-8x7b, llama2-70b
- **OpenAI**: gpt-4, gpt-3.5-turbo
- **Anthropic**: claude-3, claude-2.1
- **Google**: gemini-pro

### Default Model Sequence

When no model is specified, the tool tries these models in order:

1. enhancer-llama:latest
2. codestral:latest
3. qwen2.5-coder:latest
4. deepseek-r1:latest
5. phi4:latest
6. command-r7b:latest
7. llama3.2:latest
8. olmo2:latest

### Model Selection Strategy

- **For speed**: Use phi4:latest, command-r7b:latest
- **For quality**: Use codestral:latest, qwen2.5-coder:latest
- **For reasoning**: Use deepseek-r1:latest
- **For custom optimization**: Use enhancer-llama:latest

## Configuration & Setup

### Environment Variables

Create a `.env` file in the project root (not committed to git):

```bash
# Cloud provider API keys (optional, only if using cloud models)
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

**Security Note:** API keys are loaded via `python-dotenv` and never logged or committed.

### Output Directories

**Analysis Reports:**
- Location: `ENHANCER/analysis_reports/`
- Formats: Critical issues, improvement suggestions
- Naming: `critical_[timestamp].txt`, `suggest_[timestamp].txt`

**Logs:**
- Main log: `ENHANCER/logs/enhancer.log`
- GUI log: `ENHANCER/logs/enhancer_gui.log`
- Debug log: `logs/debug.log`

### Safe Directory Configuration

The tool restricts analysis to safe directories to prevent security issues:

- **Default Safe Dirs** (configured in `core.py`):
  - `/home/` (user directories)
  - `/tmp/` (temporary files)
  - Current working directory

**To modify:** Edit `SAFE_DIRS` constant in `ENHANCER/core.py`

## GUI Interface

### Tabbed Interface Components

1. **Files Tab** — Browse and select Python files/directories
2. **Analysis Tab** — View comprehensive code analysis results
3. **Issues Tab** — Review detected issues by severity
4. **Suggestions Tab** — AI-generated improvement suggestions
5. **Enhanced Code Tab** — View and apply suggested enhancements

### Workflow

1. **Select Files** → Browse to Python file or directory
2. **Choose Model** → Select from dropdown (Ollama or cloud)
3. **Run Analysis** → Click "Analyze" button
4. **Review Results** → Switch between tabs to see issues, suggestions
5. **Export** → Save reports for documentation/review
6. **Apply Enhancements** → Optionally apply suggested improvements

## Security Features

### Path Validation

- **Protection against**: Directory traversal attacks
- **Implementation**: Checks paths against `SAFE_DIRS` whitelist
- **Error handling**: Raises `ValueError` for invalid paths

### Content Validation

- **Protection against**: Dangerous command injection
- **Implementation**: Scans for suspicious patterns in code
- **Warning system**: Flags potentially malicious content

### Secure File Handling

- **Encoding validation**: Checks for valid UTF-8 encoding
- **Syntax validation**: Verifies Python syntax before analysis
- **Error recovery**: Graceful handling of corrupted files

## Performance Optimizations

### Parallel Processing

- **Batch Analysis**: Multiple files processed in parallel
- **Thread Pool**: Configurable worker count
- **Progress Tracking**: Real-time progress updates in GUI

### Retry Mechanisms

- **Network Failures**: Automatic retry with exponential backoff
- **Timeout Handling**: Configurable timeout settings
- **Model Fallback**: Tries next model in sequence if one fails

### Efficient Resource Usage

- **Lazy Loading**: Models loaded only when needed
- **Connection Pooling**: Reuses HTTP connections
- **Memory Management**: Clears analysis results after export

## Testing Approach

### Test Coverage (test_analyzer.py)

**File Validation Tests:**
- Invalid Python file test (non-.py extension)
- Corrupted Python file test (invalid bytes)
- Invalid encoding test (malformed UTF-8)

**Directory Validation Tests:**
- Non-existent directory handling
- Permission error handling

**Type Validation Tests:**
- Invalid auto_analyze parameter type
- Proper error raising for incorrect arguments

**Expected Results:**
- All tests should pass with "All tests completed" message
- Failures indicate core functionality regression

### Manual Testing Checklist

1. **GUI Launch** — Verify enhancer command opens GUI
2. **File Selection** — Browse to Python file successfully
3. **Model Selection** — Dropdown shows available models
4. **Analysis Execution** — Analysis completes without errors
5. **Report Export** — Reports saved to analysis_reports/
6. **Log Verification** — Logs written to logs/ directory

## Known Issues & Troubleshooting

### Issue: Model Not Found

**Symptoms:**
- "Model not found" error in GUI/CLI
- Analysis fails to start

**Solutions:**
1. Ensure Ollama is running: `ollama serve`
2. Check installed models: `ollama list`
3. Install missing model: `ollama pull codestral:latest`
4. Verify model name matches exactly (case-sensitive)

### Issue: API Key Errors

**Symptoms:**
- Cloud model authentication failures
- "Invalid API key" errors

**Solutions:**
1. Verify API keys in `.env` file
2. Check for trailing spaces in API keys
3. Ensure API keys have correct permissions
4. Test API key with provider's CLI/web interface

### Issue: Analysis Timeout

**Symptoms:**
- Analysis hangs or times out on large files
- No response after long wait

**Solutions:**
1. Try a faster model (phi4:latest, command-r7b:latest)
2. Analyze smaller code chunks
3. Increase timeout in `core.py` (default: configurable)
4. Check Ollama server logs for errors

### Issue: GUI Not Responding

**Symptoms:**
- GUI freezes during analysis
- Buttons unresponsive

**Solutions:**
1. Check logs: `ENHANCER/logs/enhancer_gui.log`
2. Ensure sufficient system memory (analysis is memory-intensive)
3. Restart Ollama server
4. Kill and relaunch GUI

### Issue: Path Validation Errors

**Symptoms:**
- "Path not in safe directories" error
- Cannot analyze files in certain locations

**Solutions:**
1. Move files to home directory or /tmp/
2. Modify `SAFE_DIRS` in `ENHANCER/core.py` to include your path
3. Run with elevated permissions (not recommended)

### Issue: Encoding Errors

**Symptoms:**
- "Invalid encoding" errors on valid Python files
- UnicodeDecodeError exceptions

**Solutions:**
1. Ensure file is UTF-8 encoded
2. Convert file encoding: `iconv -f ISO-8859-1 -t UTF-8 file.py > file_utf8.py`
3. Check for BOM (Byte Order Mark) at file start

## Recent Development History

**Latest Commits:**
- **c8a288e**: Fix unused imports in test files (cleanup)
- **7d20b04**: Complete comprehensive project rebuild and enhancement
- **cd6cdcc**: Add banner to README
- **8c3953b**: Add repository banner image
- **2e98e32**: Refactor package structure and update setup configuration

**Key Milestones:**
- Complete package restructure with ENHANCER module
- Added comprehensive test suite for analyzer
- Integrated Ollama GPU status checking
- Added multiple AI provider support (Groq, OpenAI, Anthropic, Google)
- Implemented security features (path validation, content validation)

## Next Steps & Roadmap

### Immediate Improvements

1. **Enhanced ENHANCER Package** — Add missing Python modules to repository
2. **Documentation** — Create API documentation for core modules
3. **Test Coverage** — Add unit tests for GUI components
4. **CI/CD** — Set up GitHub Actions for automated testing

### Short-Term Goals

5. **Model Management** — Auto-download missing Ollama models
6. **Report Templates** — Customizable export formats (JSON, HTML, PDF)
7. **Batch Processing** — Queue system for large directory analysis
8. **Configuration UI** — GUI settings panel for preferences

### Long-Term Vision

9. **IDE Integration** — VS Code extension for inline analysis
10. **Cloud Deployment** — Web service for remote analysis
11. **Team Features** — Shared reports, collaborative review
12. **Custom Models** — Training pipeline for domain-specific models
13. **Real-time Analysis** — Live code analysis as you type
14. **Multi-language Support** — Expand beyond Python to JavaScript, Java, etc.

## Development Patterns

### Adding a New AI Model

1. **Add to models.py** in ENHANCER package:
   ```python
   OLLAMA_MODELS = [
       "your-new-model:latest",
       # ... existing models
   ]
   ```

2. **Test model availability**:
   ```bash
   ollama pull your-new-model:latest
   ollama list  # Verify it appears
   ```

3. **Update README.md** with model description and use case

### Creating a Custom Analysis Report

1. **Extend core.py** with new report type
2. **Add export method** to GUI interface
3. **Update analysis_reports/** directory structure
4. **Document format** in README.md

### Modifying Safe Directory List

1. **Edit SAFE_DIRS** in `ENHANCER/core.py`:
   ```python
   SAFE_DIRS = [
       "/home/",
       "/tmp/",
       "/your/custom/path/",  # Add here
   ]
   ```

2. **Test path validation** with test_analyzer.py
3. **Update documentation** with security implications

## Useful Files to Know

| File | Purpose |
|------|---------|
| `setup.py` | Package configuration, dependencies, entry points |
| `ENHANCER/cli.py` | Command-line interface implementation |
| `ENHANCER/gui.py` | Tkinter GUI implementation |
| `ENHANCER/models.py` | AI model configuration and selection |
| `ENHANCER/core.py` | Core analysis engine and orchestration |
| `ENHANCER/code_analyzer.py` | Code analysis logic and validation |
| `test_analyzer.py` | Test suite for analyzer functionality |
| `check_ollama.py` | Ollama GPU and model status checker |
| `.vscode/settings.json` | Python linting configuration |
| `.gitignore` | Git ignore patterns (excludes .env, .aider*) |

## Code Quality Standards

### Linting Configuration

**Flake8:**
- Ignores E501 (line too long)
- Max line length: 999999 (effectively unlimited)

**Pylint:**
- Max line length: 999999

**Rationale:** Allows AI-generated code with long expressions, complex comprehensions, and detailed docstrings without artificial line breaks.

### Type Hints

**Recommendation:** Add type hints for better IDE support and documentation:
```python
from typing import List, Dict, Optional

def analyze_file(
    file_path: str,
    model: Optional[str] = None,
    auto_analyze: bool = False
) -> Dict[str, List[str]]:
    """Analyze a Python file for issues."""
    pass
```

### Docstrings

**Format:** Use triple-quoted strings with clear descriptions:
```python
"""
Analyze Python code for quality issues, security vulnerabilities,
and best practices.

Args:
    file_path: Path to Python file
    model: AI model to use (default: enhancer-llama:latest)
    auto_analyze: Run analysis automatically (default: False)

Returns:
    Dict containing issues, suggestions, and enhanced code

Raises:
    FileNotFoundError: If file does not exist
    ValueError: If path is not in safe directories
"""
```

## Git Workflow

### Branch Strategy

- **master** — Main development branch
- **Feature branches** — Created by Claude Code for reviews (e.g., `claude/comprehensive-project-review-*`)

### Commit Messages

**Format:** Clear, descriptive, imperative mood:
- ✅ "Add Ollama GPU status checker"
- ✅ "Fix unused imports in test files"
- ✅ "Refactor package structure for setuptools"
- ❌ "Updated stuff"
- ❌ "Fixed bug"

### Pre-commit Checklist

Before committing:
1. Run tests: `python test_analyzer.py`
2. Check imports: Verify no unused imports
3. Update README.md if adding features
4. Verify .gitignore excludes secrets (.env files)
5. Test installation: `pip install -e .`

---

**Last Updated:** October 26, 2025
**Python Version:** 3.8+
**License:** MIT
**Author:** Roo
**Repository:** https://github.com/jtgsystems/CleanCode
