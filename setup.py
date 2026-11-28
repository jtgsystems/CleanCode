"""
Setup configuration for ENHANCER package.
"""

from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="ENHANCER",  # Package name as specified in instructions
    version="1.0.0",  # Version information
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "groq>=0.3.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "google-generativeai>=0.1.0",
        "python-dotenv>=0.19.0",
        "tiktoken>=0.5.0",
        "ollama>=0.1.0",
        # tkinter is part of the standard library and not listed in install_requires
    ],
    entry_points={
        "console_scripts": [
            "enhancer=ENHANCER.cli:main",  # CLI interface
        ],
        "gui_scripts": [
            "enhancer-gui=ENHANCER.gui:main",  # GUI interface
        ],
    },
    python_requires=">=3.8",
    author="Roo",
    author_email="",  # Add author email if available
    description="Advanced Code Analysis & Enhancement Tool using multiple AI models",
    url="https://github.com/username/CleanCode",  # Replace with actual repository URL if available
    # Use try/except to handle the case where README.md might not exist
    long_description=(
        Path("README.md").read_text(encoding="utf-8")
        if Path("README.md").exists()
        else ""
    ),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Environment :: X11 Applications :: Tk",
    ],
    include_package_data=True,
    package_data={
        "ENHANCER": [
            "analysis_reports/*",
            "logs/*",
            "*.modelfile",  # Include model files
            "*.py",
        ],
    },
    # Add keywords for better discoverability
    keywords="code analysis, code enhancement, AI, code quality, security, best practices",
)
