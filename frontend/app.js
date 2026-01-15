// API Configuration
const API_URL = 'http://localhost:8000';

// State
let displayExpression = ''; // The full expression shown to user (e.g., "1+2*3")
let lastResult = null; // Store last calculation result

// DOM Elements
const expressionDisplay = document.getElementById('expression');
const resultDisplay = document.getElementById('result');
const historyList = document.getElementById('historyList');
const statusMessage = document.getElementById('statusMessage');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    updateDisplay();
});

// Number input
function appendNumber(num) {
    // If starting fresh after a calculation, clear the display
    if (lastResult !== null && displayExpression === lastResult.toString()) {
        displayExpression = '';
        lastResult = null;
    }

    displayExpression += num;
    updateDisplay();
}

// Operator input
function appendOperator(operator) {
    // Special handling for square root (unary operation)
    if (operator === 'sqrt') {
        handleSquareRoot();
        return;
    }

    // Don't add operator if expression is empty or already ends with an operator
    if (displayExpression === '') {
        return;
    }

    const lastChar = displayExpression.slice(-1);
    const operatorSymbols = ['+', '−', '×', '÷', '^'];

    // If last character is already an operator, replace it
    if (operatorSymbols.includes(lastChar)) {
        displayExpression = displayExpression.slice(0, -1);
    }

    const symbol = getOperatorSymbol(operator);
    displayExpression += symbol;
    lastResult = null;
    updateDisplay();
}

// Handle square root operation
async function handleSquareRoot() {
    const currentNumber = getCurrentNumber();
    if (currentNumber === null || currentNumber === '') {
        return;
    }

    try {
        const result = await sendCalculation('sqrt', parseFloat(currentNumber), null);
        displayExpression = result.toString();
        lastResult = result;
        updateDisplay();
        await loadHistory();
    } catch (error) {
        showError(error.message);
    }
}

// Get the current number being entered (after the last operator)
function getCurrentNumber() {
    const operatorSymbols = ['+', '−', '×', '÷', '^'];
    let currentNum = '';

    for (let i = displayExpression.length - 1; i >= 0; i--) {
        const char = displayExpression[i];
        if (operatorSymbols.includes(char)) {
            break;
        }
        currentNum = char + currentNum;
    }

    return currentNum;
}

// Backspace - delete last character
function backspace() {
    if (displayExpression.length > 0) {
        displayExpression = displayExpression.slice(0, -1);
        updateDisplay();
    }
}

// Clear display
function clearDisplay() {
    displayExpression = '';
    lastResult = null;
    updateDisplay();
}

// Parse expression into tokens (numbers and operators)
function parseExpression(expr) {
    const tokens = [];
    let currentNumber = '';

    for (let i = 0; i < expr.length; i++) {
        const char = expr[i];

        if (char >= '0' && char <= '9' || char === '.') {
            currentNumber += char;
        } else if (char === '−' && currentNumber === '' && (i === 0 || ['+', '−', '×', '÷', '^'].includes(expr[i-1]))) {
            // Handle negative numbers
            currentNumber += '-';
        } else if (['+', '−', '×', '÷', '^'].includes(char)) {
            if (currentNumber !== '') {
                tokens.push({ type: 'number', value: parseFloat(currentNumber) });
                currentNumber = '';
            }
            tokens.push({ type: 'operator', value: char });
        }
    }

    if (currentNumber !== '') {
        tokens.push({ type: 'number', value: parseFloat(currentNumber) });
    }

    return tokens;
}

// Convert display symbol to API operation name
function symbolToOperation(symbol) {
    const symbolMap = {
        '+': 'add',
        '−': 'subtract',
        '×': 'multiply',
        '÷': 'divide',
        '^': 'power',
        'mod': 'modulo'
    };
    return symbolMap[symbol] || symbol;
}

// Calculate the expression
async function calculate() {
    if (displayExpression === '' || displayExpression === '0') {
        return;
    }

    // Check if expression ends with an operator
    const lastChar = displayExpression.slice(-1);
    if (['+', '−', '×', '÷', '^'].includes(lastChar)) {
        showError('Expression cannot end with an operator');
        return;
    }

    try {
        const tokens = parseExpression(displayExpression);

        if (tokens.length === 0) {
            return;
        }

        // If there's only one number, just display it
        if (tokens.length === 1 && tokens[0].type === 'number') {
            lastResult = tokens[0].value;
            displayExpression = formatNumber(lastResult);
            updateDisplay();
            return;
        }

        // Evaluate left-to-right
        let result = tokens[0].value;

        for (let i = 1; i < tokens.length; i += 2) {
            if (i + 1 >= tokens.length) {
                break; // Incomplete expression
            }

            const operator = tokens[i].value;
            const nextNumber = tokens[i + 1].value;
            const operation = symbolToOperation(operator);

            // Send calculation to backend
            result = await sendCalculation(operation, result, nextNumber);
        }

        lastResult = result;
        displayExpression = formatNumber(result);
        updateDisplay();
        await loadHistory();

    } catch (error) {
        showError(error.message);
        // Don't clear expression on error, let user fix it
    }
}

// Send calculation to API
async function sendCalculation(operation, num1, num2) {
    const requestBody = {
        operation: operation,
        num1: num1
    };

    if (num2 !== null && num2 !== undefined) {
        requestBody.num2 = num2;
    }

    const response = await fetch(`${API_URL}/calculate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Calculation failed');
    }

    return data.result;
}

// Update display
function updateDisplay() {
    if (displayExpression === '') {
        expressionDisplay.textContent = '0';
        resultDisplay.textContent = '0';
    } else {
        expressionDisplay.textContent = displayExpression;
        resultDisplay.textContent = displayExpression;
    }
}

// Load history
async function loadHistory() {
    try {
        const response = await fetch(`${API_URL}/history`);
        const data = await response.json();

        if (data.history && data.history.length > 0) {
            displayHistory(data.history);
        } else {
            historyList.innerHTML = '<div class="empty-state">No calculations yet</div>';
        }
    } catch (error) {
        console.error('Failed to load history:', error);
        historyList.innerHTML = '<div class="empty-state">Failed to load history</div>';
    }
}

// Display history
function displayHistory(history) {
    historyList.innerHTML = '';

    history.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.onclick = () => useHistoryItem(item);

        const expression = formatHistoryExpression(item);
        const timestamp = new Date(item.timestamp).toLocaleString();

        historyItem.innerHTML = `
            <div class="history-expression">${expression}</div>
            <div class="history-result">= ${formatNumber(item.result)}</div>
            <div class="history-timestamp">${timestamp}</div>
        `;

        historyList.appendChild(historyItem);
    });
}

// Format history expression
function formatHistoryExpression(item) {
    if (item.operation === 'sqrt') {
        return `√${formatNumber(item.num1)}`;
    }
    return `${formatNumber(item.num1)} ${getOperatorSymbol(item.operation)} ${formatNumber(item.num2)}`;
}

// Use history item
function useHistoryItem(item) {
    displayExpression = item.result.toString();
    lastResult = item.result;
    updateDisplay();
}

// Clear history
async function clearHistory() {
    if (!confirm('Are you sure you want to clear all history?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/history`, {
            method: 'DELETE',
        });

        if (response.ok) {
            historyList.innerHTML = '<div class="empty-state">No calculations yet</div>';
            showSuccess('History cleared');
        } else {
            showError('Failed to clear history');
        }
    } catch (error) {
        showError('Failed to clear history');
    }
}

// Get operator symbol for display
function getOperatorSymbol(operator) {
    const symbols = {
        'add': '+',
        'subtract': '−',
        'multiply': '×',
        'divide': '÷',
        'modulo': 'mod',
        'power': '^',
        'sqrt': '√'
    };
    return symbols[operator] || operator;
}

// Format number for display
function formatNumber(num) {
    if (typeof num !== 'number') {
        num = parseFloat(num);
    }

    if (isNaN(num)) {
        return '0';
    }

    // Round to 10 decimal places to avoid floating point errors
    num = Math.round(num * 10000000000) / 10000000000;

    // Format with thousands separators for large numbers
    if (Math.abs(num) >= 1000) {
        return num.toLocaleString('en-US', { maximumFractionDigits: 10 });
    }

    return num.toString();
}

// Show success message
function showSuccess(message) {
    statusMessage.textContent = message;
    statusMessage.className = 'status-message success show';
    setTimeout(() => {
        statusMessage.classList.remove('show');
    }, 3000);
}

// Show error message
function showError(message) {
    statusMessage.textContent = message;
    statusMessage.className = 'status-message error show';
    setTimeout(() => {
        statusMessage.classList.remove('show');
    }, 3000);
}

// Keyboard support
document.addEventListener('keydown', (event) => {
    const key = event.key;

    if (key >= '0' && key <= '9') {
        appendNumber(key);
    } else if (key === '.') {
        appendNumber('.');
    } else if (key === '+') {
        appendOperator('add');
    } else if (key === '-') {
        appendOperator('subtract');
    } else if (key === '*') {
        appendOperator('multiply');
    } else if (key === '/') {
        event.preventDefault();
        appendOperator('divide');
    } else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculate();
    } else if (key === 'Backspace') {
        event.preventDefault();
        backspace();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    }
});
