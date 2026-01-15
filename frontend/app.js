// API Configuration
const API_URL = 'http://localhost:8000';

// State
let currentExpression = '';
let currentNumber = '';
let currentOperator = null;
let firstNumber = null;
let waitingForSecond = false;

// DOM Elements
const expressionDisplay = document.getElementById('expression');
const resultDisplay = document.getElementById('result');
const historyList = document.getElementById('historyList');
const statusMessage = document.getElementById('statusMessage');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
});

// Number input
function appendNumber(num) {
    if (waitingForSecond && currentNumber === '') {
        currentNumber = num;
    } else {
        currentNumber = currentNumber === '0' ? num : currentNumber + num;
    }
    updateDisplay();
}

// Operator input
function appendOperator(operator) {
    if (operator === 'sqrt') {
        // Square root is a unary operation
        if (currentNumber) {
            firstNumber = parseFloat(currentNumber);
            currentOperator = operator;
            currentExpression = `√${currentNumber}`;
            calculate();
        }
        return;
    }

    if (currentNumber !== '') {
        if (firstNumber !== null && currentOperator && !waitingForSecond) {
            // Chain calculations
            calculate();
        } else {
            firstNumber = parseFloat(currentNumber);
        }
        currentOperator = operator;
        currentExpression = `${currentNumber} ${getOperatorSymbol(operator)}`;
        currentNumber = '';
        waitingForSecond = true;
        updateDisplay();
    }
}

// Clear display
function clearDisplay() {
    currentExpression = '';
    currentNumber = '';
    currentOperator = null;
    firstNumber = null;
    waitingForSecond = false;
    resultDisplay.textContent = '0';
    expressionDisplay.textContent = '0';
}

// Calculate
async function calculate() {
    if (currentOperator === 'sqrt') {
        // Handle square root
        try {
            const result = await sendCalculation('sqrt', firstNumber, null);
            displayResult(result);
            resetAfterCalculation(result);
        } catch (error) {
            showError(error.message);
        }
        return;
    }

    if (firstNumber === null || currentOperator === null) {
        return;
    }

    const secondNumber = parseFloat(currentNumber);
    if (isNaN(secondNumber) && currentOperator !== 'sqrt') {
        showError('Invalid number');
        return;
    }

    currentExpression = `${firstNumber} ${getOperatorSymbol(currentOperator)} ${secondNumber}`;
    updateDisplay();

    try {
        const result = await sendCalculation(currentOperator, firstNumber, secondNumber);
        displayResult(result);
        resetAfterCalculation(result);
        await loadHistory(); // Refresh history
    } catch (error) {
        showError(error.message);
    }
}

// Send calculation to API
async function sendCalculation(operation, num1, num2) {
    const requestBody = {
        operation: operation,
        num1: num1
    };

    if (num2 !== null) {
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

// Display result
function displayResult(result) {
    resultDisplay.textContent = formatNumber(result);
}

// Reset after calculation
function resetAfterCalculation(result) {
    firstNumber = result;
    currentNumber = result.toString();
    currentOperator = null;
    waitingForSecond = false;
}

// Update display
function updateDisplay() {
    if (currentExpression) {
        expressionDisplay.textContent = currentExpression + (currentNumber && !waitingForSecond ? ` ${currentNumber}` : '');
    } else {
        expressionDisplay.textContent = '0';
    }
    resultDisplay.textContent = currentNumber || '0';
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
    currentNumber = item.result.toString();
    firstNumber = item.result;
    currentExpression = '';
    currentOperator = null;
    waitingForSecond = false;
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
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    }
});
