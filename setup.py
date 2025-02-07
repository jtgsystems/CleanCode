"""Setup configuration for software_enhancer package."""

from setuptools import find_packages, setup

setup(
    name="software_enhancer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "enhance=software_enhancer.main:main",
        ],
    },
    python_requires=">=3.8",
    description=("A tool for automated code enhancement " "using multiple AI models"),
    author="Roo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
