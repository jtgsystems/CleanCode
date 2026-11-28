# Change Log

All notable changes to the "enhancer-code-intelligence" extension will be documented in this file.

## [1.0.0] - 2025-11-05

### Added
- 🎉 Initial release of ENHANCER Code Intelligence
- Real-time code analysis for Python files
- Support for 30+ Ollama models + cloud providers (OpenAI, Anthropic, Google, Groq)
- Security vulnerability detection
- Code quality assessment
- Performance analysis
- AI-powered improvement suggestions
- Sidebar with tree views for:
  - Analysis Results (organized by severity)
  - AI Models (selection and management)
  - Code Metrics (LOC, file size, etc.)
- Status bar integration with analysis status
- Inline diagnostics with VS Code Problems panel integration
- Configurable real-time analysis with debouncing
- Workspace-wide analysis support
- Report export functionality (JSON/text)
- Context menu integration
- Command palette commands
- Webview panel for detailed suggestions
- Customizable severity filtering
- File size limits for analysis
- Syntax highlighting for issues

### Configuration Options
- `enhancer.enableRealTimeAnalysis` - Toggle real-time analysis
- `enhancer.analysisDelay` - Debounce delay in milliseconds
- `enhancer.defaultModel` - Default AI model selection
- `enhancer.pythonPath` - Python interpreter path
- `enhancer.enableSecurityScanning` - Toggle security scanning
- `enhancer.enablePerformanceAnalysis` - Toggle performance analysis
- `enhancer.maxFileSize` - Maximum file size to analyze
- `enhancer.showInlineHints` - Toggle inline code hints
- `enhancer.severityLevel` - Minimum severity level to display

### Commands
- `enhancer.analyzeFile` - Analyze current file
- `enhancer.analyzeWorkspace` - Analyze entire workspace
- `enhancer.showSuggestions` - Show AI suggestions
- `enhancer.selectModel` - Select AI model
- `enhancer.exportReport` - Export analysis report
- `enhancer.clearDiagnostics` - Clear all diagnostics

### Features
- Background analysis with progress indication
- Automatic analysis on file save
- Analysis on active editor change
- Model recommendations based on task
- Color-coded severity levels
- Clickable tree items to jump to issues
- Tooltip details for issues and models
- Error handling with user-friendly messages

## [Unreleased]

### Planned Features
- Quick fixes and code actions
- Support for JavaScript/TypeScript
- Custom analysis rules
- Team sharing of analysis reports
- Integration with CI/CD pipelines
- Code complexity metrics visualization
- Historical analysis tracking
- Multi-file refactoring suggestions
- Automated fix application
- Custom model training interface
