from collections import deque
from typing import Deque, Optional
from datetime import datetime
from app.models import CalculationResponse


class HistoryManager:
    """Manages calculation history with a maximum of 25 entries"""

    def __init__(self, max_size: int = 25):
        """
        Initialize history manager

        Args:
            max_size: Maximum number of history entries to keep
        """
        self.max_size = max_size
        self._history: Deque[CalculationResponse] = deque(maxlen=max_size)

    def add_calculation(
        self,
        operation: str,
        num1: float,
        num2: Optional[float],
        result: float,
        timestamp: str
    ) -> None:
        """
        Add a calculation to history

        Args:
            operation: The operation performed
            num1: First operand
            num2: Second operand (None for single operand operations)
            result: Result of the calculation
            timestamp: Timestamp of the calculation
        """
        calculation = CalculationResponse(
            operation=operation,
            num1=num1,
            num2=num2,
            result=result,
            timestamp=timestamp
        )
        # appendleft to keep most recent first
        self._history.appendleft(calculation)

    def get_history(self) -> list[CalculationResponse]:
        """
        Get calculation history (most recent first)

        Returns:
            List of calculation responses
        """
        return list(self._history)

    def clear_history(self) -> None:
        """Clear all calculation history"""
        self._history.clear()

    def get_count(self) -> int:
        """Get number of items in history"""
        return len(self._history)


# Global history manager instance
history_manager = HistoryManager()
