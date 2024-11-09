""" tests/test_calculator.py """
import math
import sys
from io import StringIO
from app.calculator import calculator

# Helper function to capture print statements
def run_calculator_with_input(monkeypatch, inputs):
    """
    Simulates user input and captures output from the calculator REPL.

    :param monkeypatch: pytest fixture to simulate user input
    :param inputs: list of inputs to simulate
    :return: captured output as a string
    """
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    # Capture the output of the calculator
    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        calculator()
    except StopIteration:
        pass  # In case inputs are exhausted without 'exit'
    sys.stdout = sys.__stdout__  # Reset stdout
    return captured_output.getvalue()

# Existing Positive Tests
def test_addition(monkeypatch):
    """Test addition operation in REPL."""
    inputs = ["add 5.0 3.0", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 8.0" in output

def test_subtraction(monkeypatch):
    """Test subtraction operation in REPL."""
    inputs = ["sub 5 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 3.0" in output

def test_multiplication(monkeypatch):
    """Test multiplication operation in REPL."""
    inputs = ["multi 4 5", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 20.0" in output

def test_division(monkeypatch):
    """Test division operation in REPL."""
    inputs = ["div 10 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

def test_exponent(monkeypatch):
    """Test addition operation in REPL."""
    inputs = ["expo 2 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 8.0" in output

def test_modulus(monkeypatch):
    """Test addition operation in REPL."""
    inputs = ["mod 5 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 1.0" in output
# Additional Tests
def test_divide_by_zero(monkeypatch):
    """Test division by zero error handling."""
    inputs = ["div 10 0", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Division by zero is not allowed." in output

def test_exponent_negative(monkeypatch):
    inputs = ["expo 2 -3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 0.125" in output

def test_exponent_negative(monkeypatch):
    inputs = ["expo -2 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: -8.0" in output

def test_invalid_command_similar_to_valid(monkeypatch):
    """Test invalid command similar to a valid one."""
    inputs = ["ad 2 3", "exit"]  # Typo in 'add'
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Unknown operation. Supported operations: add, subtract, multiply, divide, exponent, modulus." in output

def test_help(monkeypatch):
    """Test the help feature."""
    inputs = ["help", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "History Features: undo, clear, history, save, load.\nMath Functions: add, sub, multi, div, expo, mod." in output

def test_no_input(monkeypatch):
    """Test for no input."""
    inputs = ["", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "No input detected. Please enter a valid command or operation." in output

# Existing Negative Tests
def test_negative_numbers(monkeypatch):
    """Test operations with negative numbers."""
    # Test addition with negative numbers
    inputs = ["add -2 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 1.0" in output

    # Test subtraction with negative numbers
    inputs = ["sub -5 -2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: -3.0" in output

    # Test multiplication with negative numbers
    inputs = ["multi -4 5", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: -20.0" in output

    # Test division with negative numbers
    inputs = ["div -10 -2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

def test_floating_point_numbers(monkeypatch):
    """Test operations with floating point numbers."""
    # Test addition
    inputs = ["add 2.5 3.1", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.6" in output

    # Test subtraction
    inputs = ["sub 5.5 2.2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 3.3" in output

    # Test multiplication
    inputs = ["multi 4.2 5.1", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    result_line = next((line for line in output.split('\n') if "Result:" in line), None)
    assert result_line is not None, "Result not found in output"
    actual_result = float(result_line.split("Result: ")[1])
    expected_result = 21.42
    assert math.isclose(actual_result, expected_result, rel_tol=1e-5), (
        f"Expected {expected_result}, got {actual_result}"
    )
# Continuing test_calculator.py with remaining tests...

def test_history_command(monkeypatch):
    """Test the 'history' command with existing history."""
    inputs = ["add 2 3", "history", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output
    assert "Calculation History:" in output
    assert "add 2.0 3.0 = 5.0" in output

def test_history_command_no_history(monkeypatch):
    """Test the 'history' command when there is no history."""
    inputs = ["history", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Calculation History:" in output
    # Since history is empty, there should be no calculations listed

def test_clear_history(monkeypatch):
    """Test the 'clear' command."""
    inputs = ["add 2 3", "clear", "history", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output
    assert "History Cleared." in output
    assert "Calculation History:" in output
    # Ensure that history is empty after clearing
    assert "add 2.0 3.0 = 5.0" not in output

def test_undo_command(monkeypatch):
    """Test the 'undo' command."""
    inputs = ["add 2 3", "sub 5 1", "undo", "history", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Last calculation undone." in output
    assert "subtract 5.0 1.0 = 4.0" not in output
    assert "add 2.0 3.0 = 5.0" in output

def test_undo_command_empty_history(monkeypatch):
    """Test 'undo' command when history is empty."""
    inputs = ["undo", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "History is already empty." in output

def test_exit_case_insensitivity(monkeypatch):
    """Test 'exit' command in different cases."""
    # Test 'EXIT'
    inputs = ["EXIT"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Exiting calculator..." in output

    # Test 'eXiT'
    inputs = ["eXiT"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Exiting calculator..." in output

def test_incomplete_input(monkeypatch):
    """Test incomplete input handling."""
    inputs = ["add 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please follow the format: <operation> <num1> <num2>." in output

def test_extra_input(monkeypatch):
    """Test handling of extra arguments in input."""
    inputs = ["add 2 3 4", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please follow the format: <operation> <num1> <num2>." in output
    

def test_invalid_numbers(monkeypatch):
    """Test handling of invalid number inputs."""
    inputs = ["add two three", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please follow the format: <operation> <num1> <num2>." in output
    

def test_sequence_of_operations(monkeypatch):
    """Test multiple calculations and history display."""
    inputs = ["add 2 3", "multi 5 2", "history", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output
    assert "Result: 10.0" in output
    assert "Calculation History:" in output
    assert "add 2.0 3.0 = 5.0" in output
    assert "multi 5.0 2.0 = 10.0" in output

def test_clear_history_empty(monkeypatch):
    """Test 'clear' command when history is already empty."""
    inputs = ["clear", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "History Cleared." in output
    # No errors should occur when clearing an empty history

def test_unknown_command(monkeypatch):
    """Test handling of unknown commands."""
    inputs = ["unknown_command", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please follow the format: <operation> <num1> <num2>." in output

def test_division_result_precision(monkeypatch):
    """Test division result for precision."""
    inputs = ["div 1 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 0.3333333333333333" in output

def test_save_history_command(monkeypatch):
    """Test the 'save' command."""
    inputs = ["add 2 3", "save", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "History successfully saved" in output

def test_load_history_command(monkeypatch):
    """Test the 'load' command."""
    inputs = ["load", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "History successfully loaded" in output or "File was not found." in output  # Catch possible load error if file missing


