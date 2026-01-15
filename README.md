# 🧮 Vibe Calculator

A modern calculator application with a beautiful web interface and Python FastAPI backend. Features include basic arithmetic operations, advanced functions, and automatic history tracking of the last 25 calculations.

## Features

- ✨ **Modern, Beautiful UI**: Gradient design with smooth animations
- 🧮 **Basic Operations**: Addition, subtraction, multiplication, division
- 🔢 **Advanced Operations**: Power, square root
- 📝 **Expression Building**: Type full expressions (e.g., "1+1+1") before calculating
- ⌫ **Backspace Support**: Delete last character or operator with backspace button/key
- 📜 **History Tracking**: Automatically stores last 25 calculations
- ⌨️ **Keyboard Support**: Full keyboard navigation including Backspace
- 📱 **Responsive Design**: Works on desktop and mobile
- ✅ **Test-Driven Development**: Comprehensive test suite with 35 tests

## Project Structure

```
vibe-calculator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── calculator.py     # Calculator logic
│   │   ├── history.py        # History management
│   │   └── models.py         # Pydantic models
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_calculator.py
│   │   └── test_history.py
│   ├── requirements.txt
│   └── pytest.ini
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

## Prerequisites

- Python 3.11+
- Modern web browser
- pip package manager

## Installation

1. **Clone the repository**
   ```bash
   cd vibe-calculator
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Start the Frontend

Open `frontend/index.html` in your web browser, or serve it with a simple HTTP server:

```bash
cd frontend
python -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

## Running Tests

The project was built using Test-Driven Development (TDD). Run the comprehensive test suite:

```bash
cd backend
python -m pytest tests/ -v
```

All 35 tests should pass:
- 23 calculator operation tests
- 12 history tracking tests

## API Documentation

### Endpoints

#### Calculate
```
POST /calculate
Content-Type: application/json

{
  "operation": "add|subtract|multiply|divide|modulo|power|sqrt",
  "num1": float,
  "num2": float (optional for sqrt)
}
```

#### Get History
```
GET /history
```

Returns the last 25 calculations in reverse chronological order.

#### Clear History
```
DELETE /history
```

#### Health Check
```
GET /health
```

## Supported Operations

| Operation | Symbol | Example |
|-----------|--------|---------|
| Addition | + | 5 + 3 = 8 |
| Subtraction | − | 10 − 4 = 6 |
| Multiplication | × | 6 × 7 = 42 |
| Division | ÷ | 20 ÷ 4 = 5 |
| Modulo | mod | 17 mod 5 = 2 |
| Power | x^y | 2 ^ 8 = 256 |
| Square Root | √ | √16 = 4 |

## Keyboard Shortcuts

- **Numbers (0-9)**: Input numbers
- **Operators (+, -, *, /)**: Mathematical operations
- **Enter or =**: Calculate result
- **Backspace**: Delete last character or operator
- **Escape or C**: Clear calculator
- **.**: Decimal point

## Development

Built with:
- **Backend**: FastAPI, Python 3.11, Pydantic
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Testing**: Pytest, httpx

## Features in Detail

### Expression Building
- Type complete expressions before calculating (e.g., "1+1+1", "5+3×2")
- Expression remains visible until you press "=" or Enter
- Left-to-right evaluation (e.g., "5+3×2" = (5+3)×2 = 16)
- Edit expressions with backspace before calculating
- Continue calculations from previous results

### History Management
- Automatically stores successful calculations
- Displays last 25 calculations (FIFO queue)
- Click any history item to use its result
- Clear all history with one click
- Failed calculations are not stored

### Error Handling
- Division by zero protection
- Square root of negative numbers validation
- Invalid operation detection
- Missing parameter validation
- User-friendly error messages

### UI/UX
- Smooth animations and transitions
- Gradient color scheme
- Glassmorphism card design
- Hover effects and visual feedback
- Mobile-responsive layout
- Accessible design

## License

MIT License
