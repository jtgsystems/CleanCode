# ENHANCER Code Intelligence for VS Code

AI-powered code analysis with 30+ models. Get real-time security, quality, and performance insights directly in your editor.

![ENHANCER Logo](images/banner.png)

## ✨ Features

### 🔴 Real-Time Analysis
- **Instant Feedback**: Get code issues highlighted as you type
- **Smart Debouncing**: Analysis runs after you stop typing (configurable delay)
- **Background Processing**: Non-blocking analysis won't slow you down

### 🛡️ Security Scanning
- Detects dangerous patterns (`exec`, `eval`, `os.system`)
- Path traversal vulnerabilities
- Hardcoded secrets and credentials
- SQL injection risks
- OWASP Top 10 vulnerabilities

### 📊 Code Quality
- PEP 8 compliance checking
- Code complexity analysis
- Best practices adherence
- Maintainability scoring
- Dead code detection

### ⚡ Performance Analysis
- Performance bottleneck detection
- Optimization suggestions
- Algorithm complexity warnings
- Memory usage insights

### 🤖 Multiple AI Models
- **30+ Ollama models** (local, private)
- **Cloud providers**: OpenAI, Anthropic, Google, Groq
- **Model selection**: Choose the best model for your needs
- **Recommendations**: Models optimized for different tasks

### 💡 Intelligent Suggestions
- AI-generated code improvements
- Refactoring opportunities
- Modern Python features to adopt
- Performance optimizations

## 📦 Installation

### Prerequisites

1. **Python 3.8+** with ENHANCER package installed:
   ```bash
   pip install -e /path/to/CleanCode
   ```

2. **Ollama** (for local models):
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh

   # Pull recommended models
   ollama pull codestral:latest
   ollama pull qwen2.5-coder:latest
   ```

### Install Extension

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X` or `Cmd+Shift+X`)
3. Search for "ENHANCER Code Intelligence"
4. Click **Install**

**Or install from VSIX**:
```bash
code --install-extension enhancer-code-intelligence-1.0.0.vsix
```

## 🚀 Quick Start

1. **Open a Python file** in VS Code
2. **Analysis runs automatically** - look for squiggly underlines
3. **View results** in the ENHANCER sidebar (click the ENHANCER icon in Activity Bar)
4. **Hover over issues** to see details
5. **Right-click** in editor → "ENHANCER: Analyze Current File"

## ⚙️ Configuration

Open VS Code settings (`Ctrl+,` or `Cmd+,`) and search for "ENHANCER":

```json
{
  // Enable/disable real-time analysis
  "enhancer.enableRealTimeAnalysis": true,

  // Delay before analyzing (ms)
  "enhancer.analysisDelay": 1000,

  // Default AI model
  "enhancer.defaultModel": "codestral:latest",

  // Python interpreter path
  "enhancer.pythonPath": "python",

  // Enable security scanning
  "enhancer.enableSecurityScanning": true,

  // Enable performance analysis
  "enhancer.enablePerformanceAnalysis": true,

  // Maximum file size to analyze (bytes)
  "enhancer.maxFileSize": 10485760,

  // Show inline hints
  "enhancer.showInlineHints": true,

  // Minimum severity level
  "enhancer.severityLevel": "medium"
}
```

## 📋 Commands

Access via Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`):

| Command | Description |
|---------|-------------|
| `ENHANCER: Analyze Current File` | Run full analysis on active file |
| `ENHANCER: Analyze Workspace` | Analyze all Python files in workspace |
| `ENHANCER: Show Improvement Suggestions` | Get AI-generated suggestions |
| `ENHANCER: Select AI Model` | Choose which model to use |
| `ENHANCER: Export Analysis Report` | Save results to JSON/text file |
| `ENHANCER: Clear All Diagnostics` | Remove all issue markers |

## 🎨 UI Components

### Activity Bar
Click the ENHANCER icon in the Activity Bar to open the sidebar with:
- **Analysis Results**: Issues organized by severity
- **AI Models**: Available models and current selection
- **Code Metrics**: Lines of code, file size, etc.

### Status Bar
Bottom-left status bar shows:
- **Idle**: `$(code) ENHANCER` - Ready to analyze
- **Analyzing**: `$(sync~spin) Analyzing...` - Analysis in progress
- **Success**: `$(check) ✓ 5 issues found` - Analysis complete
- **Error**: `$(error) ✗ Analysis failed` - Something went wrong

### Editor Integration
- **Squiggly underlines**: Red (critical), yellow (warnings), blue (info)
- **Inline hints**: Hover to see issue details
- **Quick fixes**: Click lightbulb icon for suggested fixes
- **Context menu**: Right-click for ENHANCER commands

## 🔧 Troubleshooting

### "Python not found"
**Solution**: Set `enhancer.pythonPath` to your Python interpreter:
```json
{
  "enhancer.pythonPath": "/usr/bin/python3"
}
```

### "ENHANCER module not found"
**Solution**: Install ENHANCER package:
```bash
cd /path/to/CleanCode
pip install -e .
```

### "No models available"
**Solution**: Install Ollama and pull models:
```bash
ollama pull codestral:latest
ollama pull qwen2.5-coder:latest
```

### Analysis is slow
**Solution**:
- Use faster models (`phi4:latest`, `command-r7b:latest`)
- Increase `enhancer.analysisDelay` to reduce frequency
- Disable real-time analysis for large files

### Too many false positives
**Solution**: Adjust `enhancer.severityLevel` to `high` or `critical` to filter out low-priority issues.

## 📚 Model Recommendations

| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `enhancer-llama:latest` | General analysis | Medium | High |
| `codestral:latest` | Code quality & security | Medium | Very High |
| `qwen2.5-coder:latest` | Python-specific analysis | Fast | High |
| `deepseek-r1:latest` | Complex reasoning | Slow | Very High |
| `phi4:latest` | Quick checks | Very Fast | Good |
| `command-r7b:latest` | Real-time analysis | Very Fast | Good |

## 🤝 Contributing

Found a bug or have a feature request? Please open an issue on [GitHub](https://github.com/jtgsystems/CleanCode/issues).

## 📄 License

MIT License - See [LICENSE](https://github.com/jtgsystems/CleanCode/blob/master/LICENSE) for details.

## 🔗 Links

- **GitHub**: https://github.com/jtgsystems/CleanCode
- **Documentation**: https://github.com/jtgsystems/CleanCode#readme
- **Issues**: https://github.com/jtgsystems/CleanCode/issues
- **ENHANCER Python Package**: See main repository README

## 📸 Screenshots

### Real-Time Analysis
![Real-time analysis](images/screenshot-analysis.png)

### Sidebar Results
![Sidebar with results](images/screenshot-sidebar.png)

### Code Suggestions
![AI suggestions](images/screenshot-suggestions.png)

---

**Made with ❤️ by jtgsystems**
