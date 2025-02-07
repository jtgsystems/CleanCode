#!/usr/bin/env python3
"""Entry point script for the Software Enhancement Pipeline."""

from software_enhancer.gui import EnhancerGUI


def main():
    """Launch the Software Enhancement Pipeline application."""
    app = EnhancerGUI()
    app.run()


if __name__ == "__main__":
    main()
