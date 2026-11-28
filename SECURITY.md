## Security Policy

### Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

### Security Features

ENHANCER implements several security measures:

1. **Path Validation**: All file paths are validated against a whitelist of safe directories to prevent path traversal attacks.
2. **Content Validation**: Code content is scanned for dangerous patterns (eval, exec, sudo, rm -rf, etc.) before processing.
3. **API Key Protection**: API keys are read from environment variables only, never hardcoded.
4. **Input Sanitization**: File names and user inputs are sanitized to prevent injection attacks.
5. **Safe Subprocess Execution**: Where system commands are needed, full paths are used instead of relying on PATH.

### Security Best Practices for Users

1. **API Keys**: Store all API keys in environment variables or a `.env` file. Never commit them to version control.
   ```bash
   export GROQ_API_KEY=your_key_here
   export OPENAI_API_KEY=your_key_here
   export ANTHROPIC_API_KEY=your_key_here
   export GOOGLE_API_KEY=your_key_here
   ```

2. **Safe Directories**: The tool restricts analysis to safe directories. Modify `SAFE_DIRS` in `config.py` if you need to analyze code in other locations.

3. **Code Review**: Always review AI-generated code suggestions before applying them. The tool provides analysis and suggestions but does not automatically modify your code without explicit user action.

4. **Network Security**: When using cloud AI providers, ensure you're on a secure network. The tool uses HTTPS for all API communications.

5. **Temporary Files**: Temporary files are created in `/tmp` by default. On shared systems, consider using a user-specific temporary directory.

### Known Limitations

1. **AI Model Trust**: Analysis quality depends on the AI model used. Different models may provide different results.
2. **Offline Mode**: When using cloud models, internet connectivity is required. For offline use, use local Ollama models.
3. **Large Files**: Files larger than 10MB are skipped to prevent memory issues.

### Reporting Security Issues

If you discover a security vulnerability, please report it by:

1. **DO NOT** open a public GitHub issue
2. Email the maintainers directly with details
3. Include steps to reproduce the vulnerability
4. Allow reasonable time for a fix before public disclosure

### Security Checklist for Contributors

Before contributing code, ensure:

- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user-provided data
- [ ] Proper error handling that doesn't leak sensitive information
- [ ] Dependencies are up-to-date and free of known vulnerabilities
- [ ] New features follow the existing security patterns

### Regular Security Maintenance

- Dependencies are updated monthly
- Security scans are run with ruff's bandit rules (S-prefix)
- Code is reviewed for security issues before releases

### Vulnerability Scanning

Run security checks locally:

```bash
# Scan for security issues
ruff check ENHANCER/ --select S

# Check dependencies for known vulnerabilities
pip list --outdated
```
