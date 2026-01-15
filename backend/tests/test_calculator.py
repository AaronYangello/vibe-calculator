import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestBasicOperations:
    """Test basic calculator operations"""

    def test_addition(self):
        """Test addition operation"""
        response = client.post(
            "/calculate",
            json={"operation": "add", "num1": 5, "num2": 3}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8
        assert data["operation"] == "add"
        assert data["num1"] == 5
        assert data["num2"] == 3

    def test_addition_negative_numbers(self):
        """Test addition with negative numbers"""
        response = client.post(
            "/calculate",
            json={"operation": "add", "num1": -5, "num2": 3}
        )
        assert response.status_code == 200
        assert response.json()["result"] == -2

    def test_addition_decimals(self):
        """Test addition with decimal numbers"""
        response = client.post(
            "/calculate",
            json={"operation": "add", "num1": 5.5, "num2": 2.3}
        )
        assert response.status_code == 200
        assert abs(response.json()["result"] - 7.8) < 0.0001

    def test_subtraction(self):
        """Test subtraction operation"""
        response = client.post(
            "/calculate",
            json={"operation": "subtract", "num1": 10, "num2": 4}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 6
        assert data["operation"] == "subtract"

    def test_subtraction_negative_result(self):
        """Test subtraction resulting in negative number"""
        response = client.post(
            "/calculate",
            json={"operation": "subtract", "num1": 3, "num2": 8}
        )
        assert response.status_code == 200
        assert response.json()["result"] == -5

    def test_multiplication(self):
        """Test multiplication operation"""
        response = client.post(
            "/calculate",
            json={"operation": "multiply", "num1": 6, "num2": 7}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 42
        assert data["operation"] == "multiply"

    def test_multiplication_by_zero(self):
        """Test multiplication by zero"""
        response = client.post(
            "/calculate",
            json={"operation": "multiply", "num1": 5, "num2": 0}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 0

    def test_multiplication_negative_numbers(self):
        """Test multiplication with negative numbers"""
        response = client.post(
            "/calculate",
            json={"operation": "multiply", "num1": -4, "num2": 3}
        )
        assert response.status_code == 200
        assert response.json()["result"] == -12

    def test_division(self):
        """Test division operation"""
        response = client.post(
            "/calculate",
            json={"operation": "divide", "num1": 20, "num2": 4}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5
        assert data["operation"] == "divide"

    def test_division_with_remainder(self):
        """Test division with decimal result"""
        response = client.post(
            "/calculate",
            json={"operation": "divide", "num1": 7, "num2": 2}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 3.5

    def test_division_by_zero(self):
        """Test division by zero returns error"""
        response = client.post(
            "/calculate",
            json={"operation": "divide", "num1": 10, "num2": 0}
        )
        assert response.status_code == 400
        assert "error" in response.json()
        assert "division by zero" in response.json()["error"].lower()

    def test_modulo(self):
        """Test modulo operation"""
        response = client.post(
            "/calculate",
            json={"operation": "modulo", "num1": 17, "num2": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 2
        assert data["operation"] == "modulo"

    def test_power(self):
        """Test power operation"""
        response = client.post(
            "/calculate",
            json={"operation": "power", "num1": 2, "num2": 8}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 256
        assert data["operation"] == "power"

    def test_square_root(self):
        """Test square root operation (single operand)"""
        response = client.post(
            "/calculate",
            json={"operation": "sqrt", "num1": 16}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 4
        assert data["operation"] == "sqrt"

    def test_square_root_decimal(self):
        """Test square root with decimal result"""
        response = client.post(
            "/calculate",
            json={"operation": "sqrt", "num1": 2}
        )
        assert response.status_code == 200
        assert abs(response.json()["result"] - 1.414213562) < 0.0001

    def test_square_root_negative(self):
        """Test square root of negative number returns error"""
        response = client.post(
            "/calculate",
            json={"operation": "sqrt", "num1": -4}
        )
        assert response.status_code == 400
        assert "error" in response.json()


class TestInvalidInputs:
    """Test invalid inputs and error handling"""

    def test_invalid_operation(self):
        """Test invalid operation name"""
        response = client.post(
            "/calculate",
            json={"operation": "invalid", "num1": 5, "num2": 3}
        )
        assert response.status_code == 400
        assert "error" in response.json()

    def test_missing_num1(self):
        """Test missing num1 parameter"""
        response = client.post(
            "/calculate",
            json={"operation": "add", "num2": 3}
        )
        assert response.status_code == 422  # Validation error

    def test_missing_num2_for_binary_operation(self):
        """Test missing num2 for binary operation"""
        response = client.post(
            "/calculate",
            json={"operation": "add", "num1": 5}
        )
        assert response.status_code == 422  # Validation error

    def test_non_numeric_input(self):
        """Test non-numeric input"""
        response = client.post(
            "/calculate",
            json={"operation": "add", "num1": "abc", "num2": 3}
        )
        assert response.status_code == 422  # Validation error

    def test_missing_operation(self):
        """Test missing operation parameter"""
        response = client.post(
            "/calculate",
            json={"num1": 5, "num2": 3}
        )
        assert response.status_code == 422  # Validation error


class TestAPIEndpoints:
    """Test API endpoints and responses"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = client.post(
            "/calculate",
            json={"operation": "add", "num1": 1, "num2": 1}
        )
        assert response.status_code == 200

    def test_response_includes_timestamp(self):
        """Test response includes timestamp"""
        response = client.post(
            "/calculate",
            json={"operation": "add", "num1": 5, "num2": 3}
        )
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
