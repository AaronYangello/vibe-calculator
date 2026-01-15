import math
from typing import Tuple, Optional


class Calculator:
    """Calculator service for performing operations"""

    @staticmethod
    def add(num1: float, num2: float) -> float:
        """Add two numbers"""
        return num1 + num2

    @staticmethod
    def subtract(num1: float, num2: float) -> float:
        """Subtract num2 from num1"""
        return num1 - num2

    @staticmethod
    def multiply(num1: float, num2: float) -> float:
        """Multiply two numbers"""
        return num1 * num2

    @staticmethod
    def divide(num1: float, num2: float) -> float:
        """Divide num1 by num2"""
        if num2 == 0:
            raise ValueError("Division by zero is not allowed")
        return num1 / num2

    @staticmethod
    def modulo(num1: float, num2: float) -> float:
        """Calculate num1 modulo num2"""
        if num2 == 0:
            raise ValueError("Modulo by zero is not allowed")
        return num1 % num2

    @staticmethod
    def power(num1: float, num2: float) -> float:
        """Calculate num1 to the power of num2"""
        return num1 ** num2

    @staticmethod
    def sqrt(num1: float) -> float:
        """Calculate square root of num1"""
        if num1 < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(num1)

    @classmethod
    def calculate(cls, operation: str, num1: float, num2: Optional[float] = None) -> float:
        """
        Perform calculation based on operation

        Args:
            operation: The operation to perform
            num1: First operand
            num2: Second operand (optional for single operand operations)

        Returns:
            Result of the calculation

        Raises:
            ValueError: If operation is invalid or calculation fails
        """
        operations = {
            "add": lambda: cls.add(num1, num2),
            "subtract": lambda: cls.subtract(num1, num2),
            "multiply": lambda: cls.multiply(num1, num2),
            "divide": lambda: cls.divide(num1, num2),
            "modulo": lambda: cls.modulo(num1, num2),
            "power": lambda: cls.power(num1, num2),
            "sqrt": lambda: cls.sqrt(num1),
        }

        if operation not in operations:
            raise ValueError(f"Invalid operation: {operation}")

        return operations[operation]()
