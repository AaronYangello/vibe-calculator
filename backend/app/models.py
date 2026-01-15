from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Literal
from datetime import datetime


class CalculationRequest(BaseModel):
    """Request model for calculation"""
    operation: Literal["add", "subtract", "multiply", "divide", "modulo", "power", "sqrt"]
    num1: float
    num2: Optional[float] = None

    @model_validator(mode='after')
    def validate_num2(self):
        """Validate that num2 is provided for binary operations"""
        binary_ops = ["add", "subtract", "multiply", "divide", "modulo", "power"]

        if self.operation in binary_ops and self.num2 is None:
            raise ValueError(f"num2 is required for {self.operation} operation")

        return self


class CalculationResponse(BaseModel):
    """Response model for calculation"""
    operation: str
    num1: float
    num2: Optional[float] = None
    result: float
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str


class HistoryResponse(BaseModel):
    """Response model for history"""
    history: list[CalculationResponse]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str


class ClearHistoryResponse(BaseModel):
    """Clear history response"""
    message: str
