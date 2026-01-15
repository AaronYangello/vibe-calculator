# Frontend Calculator Test Specifications

## Expression Building Tests

### Test: Display single number
- **Input:** User clicks "1"
- **Expected:** Display shows "1"

### Test: Build simple expression
- **Input:** User clicks "1", "+", "1"
- **Expected:** Display shows "1+1"
- **Note:** Expression should remain visible until "=" is pressed

### Test: Build complex expression with multiple operations
- **Input:** User clicks "1", "+", "1", "+", "1"
- **Expected:** Display shows "1+1+1"

### Test: Calculate simple expression
- **Input:** User clicks "1", "+", "1", "="
- **Expected:**
  - Before "=": Display shows "1+1"
  - After "=": Display shows "3"
  - Expression scrolls away, only result remains

### Test: Calculate complex chained expression
- **Input:** User clicks "5", "+", "3", "*", "2", "="
- **Expected:**
  - Before "=": Display shows "5+3*2"
  - After "=": Display shows "16" (left-to-right evaluation: 5+3=8, 8*2=16)

### Test: Continue calculation from result
- **Input:** User clicks "5", "+", "3", "=", "+", "2", "="
- **Expected:**
  - After first "=": Display shows "8"
  - After typing "+": Display shows "8+"
  - After typing "2": Display shows "8+2"
  - After second "=": Display shows "10"

## Backspace Functionality Tests

### Test: Backspace deletes last number
- **Input:** User clicks "1", "2", "3", [Backspace]
- **Expected:** Display shows "12"

### Test: Backspace deletes operator
- **Input:** User clicks "1", "+", [Backspace]
- **Expected:** Display shows "1"

### Test: Backspace in complex expression
- **Input:** User clicks "1", "+", "2", "*", "3", [Backspace], [Backspace], [Backspace]
- **Expected:**
  - After first backspace: Display shows "1+2*"
  - After second backspace: Display shows "1+2"
  - After third backspace: Display shows "1+"

### Test: Backspace on single character
- **Input:** User clicks "5", [Backspace]
- **Expected:** Display shows "0" (cleared)

### Test: Backspace does nothing when empty
- **Input:** User clicks [Backspace] when display is empty/zero
- **Expected:** Display shows "0"

### Test: Backspace with decimal numbers
- **Input:** User clicks "1", ".", "5", "+", "2", ".", "3", [Backspace]
- **Expected:** Display shows "1.5+2."

## Error Handling Tests

### Test: Division by zero in expression
- **Input:** User clicks "1", "0", "÷", "0", "="
- **Expected:** Error message displayed, expression cleared

### Test: Invalid expression (multiple operators)
- **Input:** User clicks "+", "+", "1"
- **Expected:** Should handle gracefully (ignore or show error)

## Keyboard Support Tests

### Test: Backspace key deletes character
- **Input:** User types "123" then presses Backspace key
- **Expected:** Display shows "12"

### Test: Enter key calculates result
- **Input:** User types "1+1" then presses Enter
- **Expected:** Display shows "2"

## Implementation Notes

1. **Expression Storage**: Maintain an expression string that builds up as user inputs numbers and operators
2. **Calculation Logic**: When "=" is pressed:
   - Parse expression left-to-right
   - Perform operations sequentially (1+2*3 = (1+2)*3 = 9)
   - Send each binary operation to backend API
   - Chain results together
3. **Display Updates**: Update display after each input to show full expression
4. **Backspace Logic**: Remove last character from expression string
5. **Clear Behavior**: Preserve existing clear functionality
