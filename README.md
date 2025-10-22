![Banner](banner.png)

# CleanCode - Advanced Code Analysis & Enhancement Tool

CleanCode is a comprehensive Python-based tool that leverages multiple AI models to analyze code for potential improvements, issues, and best practices. It provides both a user-friendly Graphical User Interface (GUI) and command-line capabilities for flexible usage.

## Features

- **Comprehensive Code Analysis**:
  - Code quality issues
  - Security vulnerabilities
  - Performance considerations
  - Best practices adherence
  - Potential bugs detection
  - Maintainability issues

- **AI-Powered Enhancements**:
  - Suggests improvements based on analysis
  - Can optionally apply enhancements directly (via GUI)
  - Multiple model support for diverse perspectives

- **Multiple Model Support**:
  - Local Ollama models (30+ supported)
  - Cloud provider models (OpenAI, Claude, Groq, Google)
  - Configurable model sequence for analysis/suggestions

- **User-Friendly Interface**:
  - Intuitive Graphical User Interface
  - Tabbed interface for files, analysis, issues, suggestions, and enhanced code
  - Export capabilities for reports and issues

- **Security Features**:
  - Path validation to prevent traversal attacks
  - Content validation to detect dangerous commands
  - Secure file handling

- **Performance Optimizations**:
  - Parallel processing for batch analysis
  - Efficient retry mechanisms
  - Configurable timeout settings

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- For Ollama models: [Ollama](https://ollama.ai/) installed and running locally

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CleanCode
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

   This will install the `enhancer` command globally, which launches the GUI.

3. Set up API keys for cloud providers (optional):
   ```bash
   # Add these to your environment variables
   GROQ_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   GOOGLE_API_KEY=your_key_here
   ```

4. For Ollama models, ensure they are installed:
   ```bash
   # Check installed models
   ollama list
   
   # Install a model if needed
   ollama pull enhancer-llama:latest
   ```

## Usage

### GUI Mode

Launch the GUI from your terminal:

```bash
enhancer
```

The GUI allows you to:
- Browse and select Python files or directories
- Choose the AI model to use for analysis
- Run analysis to identify issues
- Generate improvement suggestions
- View and apply code enhancements
- Export analysis reports

### Command Line Usage

While the primary interface is GUI-based, you can also use the tool from the command line:

```bash
# Analyze a specific file
python -m ENHANCER.cli analyze path/to/file.py

# Analyze a directory
python -m ENHANCER.cli analyze path/to/directory

# Generate suggestions for a file
python -m ENHANCER.cli suggest path/to/file.py

# Specify a model to use
python -m ENHANCER.cli analyze path/to/file.py --model codestral:latest
```

## Available Models

The tool supports a wide range of models for analysis:

### Local Models (Ollama)

- enhancer-llama:latest (custom model optimized for code analysis)
- codestral:latest
- qwen2.5-coder:latest
- deepseek-r1:latest
- phi4:latest
- command-r7b:latest
- llama3.2:latest
- llama3.3:latest
- olmo2:latest
- And many more (see models.py for the complete list)

### Cloud Models (Optional)

- [Groq] mixtral-8x7b
- [Groq] llama2-70b
- [OpenAI] gpt-4
- [Claude] claude-3
- [Claude] claude-2.1
- [Google] gemini-pro

## Default Model Sequence

The tool will try these models in order when performing actions if not specified:

1. enhancer-llama:latest
2. codestral:latest
3. qwen2.5-coder:latest
4. deepseek-r1:latest
5. phi4:latest
6. command-r7b:latest
7. llama3.2:latest
8. olmo2:latest

## Configuration Options

### Output Directories

- Analysis reports: `ENHANCER/analysis_reports/`
- Logs: `ENHANCER/logs/`

### Log Files

- Main log: `ENHANCER/logs/enhancer.log`
- GUI log: `ENHANCER/logs/enhancer_gui.log`

### Analysis Reports

- Critical issues: `analysis_reports/critical_[timestamp].txt`
- Improvement suggestions: `analysis_reports/suggest_[timestamp].txt`

## Troubleshooting

### Common Issues

1. **Model Not Found**: 
   - Ensure Ollama is running (`ollama serve`)
   - Check installed models (`ollama list`)
   - Install missing models (`ollama pull model_name`)

2. **API Key Issues**:
   - Verify API keys are correctly set in environment variables
   - Check for trailing spaces in API keys
   - Ensure API keys have the correct permissions

3. **Analysis Timeout**:
   - For large files, analysis may take longer
   - Try a different model with better performance
   - Adjust timeout settings in `core.py` if needed

4. **GUI Not Responding**:
   - Check logs at `ENHANCER/logs/enhancer_gui.log`
   - Ensure you have sufficient system resources
   - Restart the application

5. **Path Validation Errors**:
   - The tool restricts analysis to safe directories
   - Modify `SAFE_DIRS` in `core.py` if needed

### Getting Help

- Check the logs for detailed error messages
- Review the source code comments for implementation details
- File an issue in the repository if you encounter persistent problems

## License

MIT License - Feel free to use and modify as needed.
