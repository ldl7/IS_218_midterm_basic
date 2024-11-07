# tests/test_history.py

import pytest
from app.history import History

def test_add_calculation():
    # Positive test: Add a calculation and verify it's in history
    history = History()
    history.add_calculation("add 2 3 = 5")
    assert history.get_history() == ["add 2 3 = 5"]

def test_add_multiple_calculations():
    # Positive test: Add multiple calculations
    history = History()
    calculations = ["add 2 3 = 5", "subtract 5 2 = 3", "multiply 2 3 = 6"]
    for calc in calculations:
        history.add_calculation(calc)
    assert history.get_history() == calculations

def test_clear_history():
    # Positive test: Clear history after adding calculations
    history = History()
    history.add_calculation("add 2 3 = 5")
    history.clear_history()
    assert history.get_history() == []

def test_undo_last():
    # Positive test: Undo the last calculation
    history = History()
    history.add_calculation("add 2 3 = 5")
    history.add_calculation("subtract 5 2 = 3")
    history.undo_last()
    assert history.get_history() == ["add 2 3 = 5"]

def test_undo_last_empty_history(capsys):
    # Negative test: Undo last calculation when history is empty
    history = History()
    history.undo_last()
    captured = capsys.readouterr()
    assert captured.out.strip() == "History is already empty."
    assert history.get_history() == []

def test_get_history():
    # Positive test: Retrieve history
    history = History()
    calculations = ["add 2 3 = 5", "multiply 4 5 = 20"]
    for calc in calculations:
        history.add_calculation(calc)
    assert history.get_history() == calculations

def test_clear_history_empty():
    # Positive test: Clear history when it's already empty
    history = History()
    history.clear_history()
    assert history.get_history() == []

def test_add_non_string_calculation():
    # Negative test: Add non-string calculation
    history = History()
    with pytest.raises(TypeError):
        history.add_calculation(12345)  # Should raise TypeError

def test_add_calculation_none():
    # Negative test: Add None as a calculation
    history = History()
    with pytest.raises(TypeError):
        history.add_calculation(None)  # Should raise TypeError

def test_get_history_is_copy():
    # Negative test: Ensure get_history returns a copy, not a reference
    history = History()
    history.add_calculation("add 1 1 = 2")
    retrieved_history = history.get_history()
    retrieved_history.append("subtract 2 1 = 1")
    assert history.get_history() == ["add 1 1 = 2"]

def test_undo_last_after_clear(capsys):
    # Negative test: Undo last after clearing history
    history = History()
    history.add_calculation("add 2 3 = 5")
    history.clear_history()
    history.undo_last()
    captured = capsys.readouterr()
    assert captured.out.strip() == "History is already empty."
    assert history.get_history() == []
