from setuptools import find_packages, setup

setup(
    name="ENHANCER",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "python-dotenv"],
    entry_points={
        "console_scripts": [
            "enhancer=ENHANCER.gui:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A code enhancement tool using AI",
    long_description="A tool for code analysis and enhancement using AI",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ENHANCER",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
