"""Sample code file for testing the analyzer."""


def calculate_sum(a, b):
    """Calculate sum of two numbers."""
    return a + b


def greet(name):
    """Greet a person."""
    # TODO: Add internationalization support
    print(f"Hello, {name}!")


class Calculator:
    """Simple calculator class."""

    def add(self, x, y):
        """Add two numbers."""
        return x + y

    def subtract(self, x, y):
        """Subtract two numbers."""
        return x - y


if __name__ == "__main__":
    calc = Calculator()
    result = calc.add(5, 3)
    print(f"Result: {result}")
