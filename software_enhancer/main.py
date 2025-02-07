"""Main entry point for the Software Enhancement Pipeline."""

from .gui import EnhancerGUI


def main():
    """Launch the Software Enhancement Pipeline application."""
    app = EnhancerGUI()
    app.run()


if __name__ == "__main__":
    main()
