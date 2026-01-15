import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCalculationHistory:
    """Test calculation history tracking"""

    def setup_method(self):
        """Clear history before each test"""
        client.delete("/history")

    def test_get_empty_history(self):
        """Test getting history when no calculations exist"""
        response = client.get("/history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)
        assert len(data["history"]) == 0

    def test_history_stores_calculation(self):
        """Test that calculation is stored in history"""
        # Perform a calculation
        calc_response = client.post(
            "/calculate",
            json={"operation": "add", "num1": 5, "num2": 3}
        )
        assert calc_response.status_code == 200

        # Check history
        history_response = client.get("/history")
        assert history_response.status_code == 200
        history = history_response.json()["history"]
        assert len(history) == 1
        assert history[0]["operation"] == "add"
        assert history[0]["num1"] == 5
        assert history[0]["num2"] == 3
        assert history[0]["result"] == 8

    def test_history_stores_multiple_calculations(self):
        """Test that multiple calculations are stored"""
        # Perform multiple calculations
        operations = [
            {"operation": "add", "num1": 5, "num2": 3},
            {"operation": "subtract", "num1": 10, "num2": 4},
            {"operation": "multiply", "num1": 6, "num2": 7},
        ]

        for op in operations:
            response = client.post("/calculate", json=op)
            assert response.status_code == 200

        # Check history
        history_response = client.get("/history")
        assert history_response.status_code == 200
        history = history_response.json()["history"]
        assert len(history) == 3

    def test_history_most_recent_first(self):
        """Test that history returns most recent calculations first"""
        # Perform calculations
        client.post("/calculate", json={"operation": "add", "num1": 1, "num2": 1})
        client.post("/calculate", json={"operation": "add", "num1": 2, "num2": 2})
        client.post("/calculate", json={"operation": "add", "num1": 3, "num2": 3})

        # Check history order
        history_response = client.get("/history")
        history = history_response.json()["history"]
        assert len(history) == 3
        # Most recent should be first
        assert history[0]["num1"] == 3
        assert history[1]["num1"] == 2
        assert history[2]["num1"] == 1

    def test_history_limited_to_25_calculations(self):
        """Test that history only stores last 25 calculations"""
        # Perform 30 calculations
        for i in range(30):
            response = client.post(
                "/calculate",
                json={"operation": "add", "num1": i, "num2": 1}
            )
            assert response.status_code == 200

        # Check history length
        history_response = client.get("/history")
        history = history_response.json()["history"]
        assert len(history) == 25

        # Check that oldest calculations were removed
        # Most recent should be calculation with num1=29
        assert history[0]["num1"] == 29
        # Oldest should be calculation with num1=5 (30-25=5)
        assert history[24]["num1"] == 5

    def test_history_includes_timestamps(self):
        """Test that history includes timestamps for each calculation"""
        client.post("/calculate", json={"operation": "add", "num1": 5, "num2": 3})

        history_response = client.get("/history")
        history = history_response.json()["history"]
        assert len(history) == 1
        assert "timestamp" in history[0]

    def test_history_includes_operation_details(self):
        """Test that history includes all operation details"""
        client.post("/calculate", json={"operation": "divide", "num1": 10, "num2": 2})

        history_response = client.get("/history")
        history = history_response.json()["history"]
        assert len(history) == 1
        entry = history[0]
        assert entry["operation"] == "divide"
        assert entry["num1"] == 10
        assert entry["num2"] == 2
        assert entry["result"] == 5
        assert "timestamp" in entry

    def test_history_does_not_store_errors(self):
        """Test that failed calculations are not stored in history"""
        # Perform a calculation that will fail
        response = client.post(
            "/calculate",
            json={"operation": "divide", "num1": 10, "num2": 0}
        )
        assert response.status_code == 400

        # Check history is empty
        history_response = client.get("/history")
        history = history_response.json()["history"]
        assert len(history) == 0

    def test_clear_history(self):
        """Test clearing calculation history"""
        # Add some calculations
        for i in range(5):
            client.post("/calculate", json={"operation": "add", "num1": i, "num2": 1})

        # Verify history has items
        history_response = client.get("/history")
        assert len(history_response.json()["history"]) == 5

        # Clear history
        clear_response = client.delete("/history")
        assert clear_response.status_code == 200
        assert "message" in clear_response.json()

        # Verify history is empty
        history_response = client.get("/history")
        assert len(history_response.json()["history"]) == 0

    def test_history_with_single_operand_operation(self):
        """Test history stores single operand operations correctly"""
        client.post("/calculate", json={"operation": "sqrt", "num1": 16})

        history_response = client.get("/history")
        history = history_response.json()["history"]
        assert len(history) == 1
        entry = history[0]
        assert entry["operation"] == "sqrt"
        assert entry["num1"] == 16
        assert entry["result"] == 4
        # num2 should be None or not present for single operand operations
        assert entry.get("num2") is None

    def test_history_persistence_across_calculations(self):
        """Test that history persists across multiple calculation requests"""
        # Perform calculations and verify history grows
        for i in range(3):
            client.post("/calculate", json={"operation": "add", "num1": i, "num2": 1})
            history_response = client.get("/history")
            history = history_response.json()["history"]
            assert len(history) == i + 1
