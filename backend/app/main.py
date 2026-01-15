from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

from app.models import (
    CalculationRequest,
    CalculationResponse,
    ErrorResponse,
    HistoryResponse,
    HealthResponse,
    ClearHistoryResponse
)
from app.calculator import Calculator
from app.history import history_manager

app = FastAPI(
    title="Calculator API",
    description="A modern calculator API with history tracking",
    version="1.0.0"
)

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with custom format"""
    # Check if this is an invalid operation value
    errors = exc.errors()
    for error in errors:
        if error.get("type") == "literal_error" and "operation" in str(error.get("loc", [])):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid operation"}
            )
        # Check if it's a value_error from our model validator (missing num2)
        if error.get("type") == "value_error":
            # Return 422 for validation errors
            # Format errors properly by converting to serializable format
            formatted_errors = []
            for e in errors:
                formatted_errors.append({
                    "type": e.get("type"),
                    "loc": e.get("loc"),
                    "msg": e.get("msg"),
                })
            return JSONResponse(
                status_code=422,
                content={"detail": formatted_errors}
            )
    # For other validation errors, return 422
    # Format errors properly
    formatted_errors = []
    for e in errors:
        formatted_errors.append({
            "type": e.get("type"),
            "loc": e.get("loc"),
            "msg": e.get("msg"),
        })
    return JSONResponse(
        status_code=422,
        content={"detail": formatted_errors}
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy")


@app.post("/calculate", response_model=CalculationResponse, responses={400: {"model": ErrorResponse}})
async def calculate(request: CalculationRequest):
    """
    Perform a calculation

    Args:
        request: Calculation request with operation and operands

    Returns:
        Calculation result with timestamp

    Raises:
        HTTPException: If calculation fails
    """
    try:
        result = Calculator.calculate(
            operation=request.operation,
            num1=request.num1,
            num2=request.num2
        )

        timestamp = datetime.utcnow().isoformat()

        # Add to history
        history_manager.add_calculation(
            operation=request.operation,
            num1=request.num1,
            num2=request.num2,
            result=result,
            timestamp=timestamp
        )

        return CalculationResponse(
            operation=request.operation,
            num1=request.num1,
            num2=request.num2,
            result=result,
            timestamp=timestamp
        )

    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except TypeError as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )


@app.get("/history", response_model=HistoryResponse)
async def get_history():
    """
    Get calculation history (last 25 calculations, most recent first)

    Returns:
        History response with list of calculations
    """
    history = history_manager.get_history()
    return HistoryResponse(history=history)


@app.delete("/history", response_model=ClearHistoryResponse)
async def clear_history():
    """
    Clear calculation history

    Returns:
        Success message
    """
    history_manager.clear_history()
    return ClearHistoryResponse(message="History cleared successfully")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
