# GitHub Actions CI/CD Workflow Setup Instructions

## ⚠️ Manual Setup Required

The GitHub Actions workflow file `.github/workflows/ci.yml` could not be automatically committed due to GitHub App permissions restrictions. This is a security feature that prevents automated tools from creating or modifying workflow files without explicit `workflows` permission.

## 📋 How to Add the CI/CD Workflow

### Option 1: Via GitHub Web Interface (Recommended)

1. Navigate to your repository on GitHub: https://github.com/jtgsystems/CleanCode
2. Click on the **"Actions"** tab
3. Click **"New workflow"** or **"Set up a workflow yourself"**
4. Copy the contents from `.github/workflows/ci.yml` (provided below)
5. Paste into the editor
6. Commit directly to the `master` or `main` branch (or create a PR)

### Option 2: Via Git with Admin Permissions

If you have admin access to the repository:

```bash
# Add the workflow file
git add .github/workflows/ci.yml

# Commit
git commit -m "ci: Add GitHub Actions workflow for automated testing and security scanning"

# Push (requires admin or workflows permission)
git push
```

### Option 3: Create a Pull Request

1. Add and commit the file locally:
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "ci: Add GitHub Actions workflow"
   git push
   ```

2. Create a pull request on GitHub
3. A repository admin can review and merge

## 📄 Workflow File Contents

The complete workflow file is located at `.github/workflows/ci.yml` in your local repository.

### What the Workflow Does

✅ **Multi-OS Testing**: Tests on Ubuntu, macOS, and Windows
✅ **Multi-Python Testing**: Tests Python versions 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
✅ **Linting**: Runs flake8 to check code quality
✅ **Formatting**: Validates code formatting with Black
✅ **Testing**: Runs pytest with coverage reporting
✅ **Security Scanning**: Runs Bandit security scanner and pip-audit
✅ **Type Checking**: Runs mypy for static type analysis
✅ **Coverage Reporting**: Uploads coverage to Codecov

### Triggers

The workflow runs on:
- Push to `master`, `main`, or `claude/*` branches
- Pull requests to `master` or `main` branches

## 🔍 Verification

Once the workflow is added, you can verify it's working by:

1. Going to the **Actions** tab on GitHub
2. Checking for a workflow run triggered by your commit
3. Reviewing the test results, coverage, and security reports

## 📝 Alternative: Manual Testing

Until the workflow is added, you can run the same checks locally:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 ENHANCER/ tests/

# Run formatting check
black --check ENHANCER/ tests/

# Run tests with coverage
pytest tests/ -v --cov=ENHANCER --cov-report=html

# Run security scanner
bandit -r ENHANCER/

# Run type checking
mypy ENHANCER/ --ignore-missing-imports

# Run dependency audit
pip-audit
```

## 🚀 Benefits of Adding the Workflow

Once added, the CI/CD workflow will:
- Automatically test all pull requests
- Catch bugs before they reach production
- Ensure code quality standards are maintained
- Detect security vulnerabilities early
- Provide coverage reports for code review
- Support multiple Python versions and operating systems

## ❓ Questions?

If you encounter issues adding the workflow, please:
1. Check your repository permissions
2. Ensure you have the `workflows` permission
3. Contact a repository administrator
4. Refer to GitHub's documentation: https://docs.github.com/en/actions

---

**Note**: This file can be deleted once the workflow is successfully added to the repository.
