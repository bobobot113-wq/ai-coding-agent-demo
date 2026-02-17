"""
Buggy Calculator - For AI Agent Demo
=====================================
A simple calculator with intentional bugs for the AI agent to identify and fix.
"""


class Calculator:
    """A simple calculator class."""
    
    def __init__(self):
        self.result = 0
    
    def add(self, a, b):
        """Add two numbers."""
        # Bug: Should return a + b
        return a - b  # Wrong operator!
    
    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        # Bug: Should return a * b
        return a + b  # Wrong operator!
    
    def divide(self, a, b):
        """Divide a by b."""
        # Bug: No zero division check
        return a / b
    
    def power(self, a, b):
        """Calculate a to the power of b."""
        # Bug: Should be a ** b
        return a * b  # Wrong operator!
    
    def modulo(self, a, b):
        """Calculate a mod b."""
        return a % b


def calculate(operator, a, b):
    """Calculate based on operator."""
    calc = Calculator()
    
    # Bug: No validation of operator
    if operator == '+':
        return calc.add(a, b)
    elif operator == '-':
        return calc.subtract(a, b)
    elif operator == '*':
        return calc.multiply(a, b)
    elif operator == '/':
        return calc.divide(a, b)
    elif operator == '**':
        return calc.power(a, b)
    elif operator == '%':
        return calc.modulo(a, b)


# Main - with bugs
if __name__ == "__main__":
    # Test calculations
    print("Testing Calculator:")
    print("5 + 3 =", calculate('+', 5, 3))   # Will show 2 (wrong!)
    print("5 * 3 =", calculate('*', 5, 3))   # Will show 8 (wrong!)
    print("2 ** 3 =", calculate('**', 2, 3))  # Will show 6 (wrong!)
    print("10 / 0 =", calculate('/', 10, 0))  # Will crash!
