"""tests/test_history.py

Unit tests for the History class.
"""

import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

import pandas as pd
import pytest

from app.history import History


# Pytest Test Functions
def test_add_calculation() -> None:
    """Test adding a calculation to history."""
    history = History()
    history.add_calculation("add 2 3 = 5")
    assert history.get_history() == ["add 2 3 = 5"]


def test_add_multiple_calculations() -> None:
    """Test adding multiple calculations to history."""
    history = History()
    calculations = [
        "add 2 3 = 5",
        "subtract 5 2 = 3",
        "multiply 2 3 = 6"
    ]
    for calc in calculations:
        history.add_calculation(calc)
    assert history.get_history() == calculations


def test_clear_history() -> None:
    """Test clearing history after adding calculations."""
    history = History()
    history.add_calculation("add 2 3 = 5")
    history.clear_history()
    assert history.get_history() == []


def test_undo_last() -> None:
    """Test undoing the last calculation."""
    history = History()
    history.add_calculation("add 2 3 = 5")
    history.add_calculation("subtract 5 2 = 3")
    history.undo_last()
    assert history.get_history() == ["add 2 3 = 5"]


def test_undo_last_empty_history(capsys: pytest.CaptureFixture) -> None:
    """Test undoing the last calculation when history is empty."""
    history = History()
    history.undo_last()
    captured = capsys.readouterr()
    assert captured.out.strip() == "History is already empty."
    assert history.get_history() == []


def test_get_history() -> None:
    """Test retrieving history."""
    history = History()
    calculations = ["add 2 3 = 5", "multiply 4 5 = 20"]
    for calc in calculations:
        history.add_calculation(calc)
    assert history.get_history() == calculations


def test_clear_history_empty() -> None:
    """Test clearing history when it is already empty."""
    history = History()
    history.clear_history()
    assert history.get_history() == []


def test_add_non_string_calculation() -> None:
    """Test adding a non-string calculation to history."""
    history = History()
    with pytest.raises(TypeError):
        history.add_calculation(12345)  # Should raise TypeError


def test_add_calculation_none() -> None:
    """Test adding None as a calculation to history."""
    history = History()
    with pytest.raises(TypeError):
        history.add_calculation(None)  # Should raise TypeError


def test_get_history_is_copy() -> None:
    """Ensure get_history returns a copy, not a reference."""
    history = History()
    history.add_calculation("add 1 1 = 2")
    retrieved_history = history.get_history()
    retrieved_history.append("subtract 2 1 = 1")
    assert history.get_history() == ["add 1 1 = 2"]


def test_undo_last_after_clear(capsys: pytest.CaptureFixture) -> None:
    """Test undoing last calculation after clearing history."""
    history = History()
    history.add_calculation("add 2 3 = 5")
    history.clear_history()
    history.undo_last()
    captured = capsys.readouterr()
    assert captured.out.strip() == "History is already empty."
    assert history.get_history() == []


# Unittest TestCase Class
class TestHistory(unittest.TestCase):
    """Unit tests for the History class's save and load methods."""

    def setUp(self) -> None:
        """Set up a temporary directory for test files."""
        self.temp_dir = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.history_file = os.path.join(self.temp_dir.name, 'history.csv')
        self.history = History()

    def tearDown(self) -> None:
        """Clean up the temporary directory after tests."""
        self.temp_dir.cleanup()

    def test_save_history_with_entries(self) -> None:
        """Test saving a history with multiple calculations to a CSV file."""
        calculations = [
            "add 2 3 = 5",
            "subtract 10 4 = 6",
            "multiply 3 7 = 21"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            expected_message = f"History successfully saved to {self.history_file}."
            self.assertIn(expected_message, fake_out.getvalue())

        df = pd.read_csv(self.history_file, dtype=str, encoding='utf-8')
        self.assertIn('calculations', df.columns, "CSV does not contain 'calculations' column.")
        self.assertEqual(
            df['calculations'].tolist(),
            calculations,
            "Saved calculations do not match the history."
        )

    def test_save_empty_history(self) -> None:
        """Test saving an empty history to a CSV file."""
        self.assertEqual(len(self.history.get_history()), 0, "History is not empty.")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            expected_message = f"History successfully saved to {self.history_file}."
            self.assertIn(expected_message, fake_out.getvalue())

        df = pd.read_csv(self.history_file, dtype=str, encoding='utf-8')
        self.assertIn('calculations', df.columns, "CSV does not contain 'calculations' column.")
        self.assertEqual(len(df), 0, "CSV file should be empty for empty history.")

    def test_load_history_with_entries(self) -> None:
        """Test loading a history from a CSV file with multiple calculations."""
        calculations = [
            "add 2 3 = 5",
            "subtract 10 4 = 6",
            "multiply 3 7 = 21"
        ]
        df = pd.DataFrame({'calculations': calculations})
        df.to_csv(self.history_file, index=False, encoding='utf-8')

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            expected_message = f"History successfully loaded from {self.history_file}."
            self.assertIn(expected_message, fake_out.getvalue())

        self.assertEqual(
            self.history.get_history(),
            calculations,
            "Loaded history does not match the CSV file."
        )

    def test_load_empty_history_file(self) -> None:
        """Test loading from an empty CSV file."""
        with open(self.history_file, 'w', encoding='utf-8') as _file:
            pass  # Create an empty file

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            output = fake_out.getvalue()

        expected_message = f"The file {self.history_file} is empty."
        self.assertIn(expected_message, output)
        self.assertEqual(len(self.history.get_history()),
        0,
        "History should remain empty after loading from an empty file."
        )

    def test_load_nonexistent_file(self) -> None:
        """Test loading history from a non-existent CSV file."""
        nonexistent_file = os.path.join(self.temp_dir.name, 'nonexistent.csv')

        self.assertFalse(os.path.exists(nonexistent_file), "File unexpectedly exists.")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(nonexistent_file)
            output = fake_out.getvalue()

        expected_message = f"The file {nonexistent_file} was not found."
        self.assertIn(expected_message, output)
        self.assertEqual(
        len(self.history.get_history()),
        0,
        "History should remain empty when loading from a non-existent file."
    )
    def test_save_and_load_cycle(self) -> None:
        """Test saving and then loading history to ensure data persistence."""
        calculations = [
            "add 1 1 = 2",
            "divide 10 2 = 5"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            expected_save_message = f"History successfully saved to {self.history_file}."
            self.assertIn(expected_save_message, fake_out.getvalue())

        new_history = History()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            new_history.load(self.history_file)
            expected_load_message = f"History successfully loaded from {self.history_file}."
            self.assertIn(expected_load_message, fake_out.getvalue())

        self.assertEqual(
            new_history.get_history(),
            calculations,
            "Loaded history does not match the original."
        )

    def test_save_overwrites_existing_file(self) -> None:
        """Test that saving history overwrites an existing CSV file."""
        initial_calculations = ["multiply 2 2 = 4"]
        df_initial = pd.DataFrame({'calculations': initial_calculations})
        df_initial.to_csv(self.history_file, index=False, encoding='utf-8')

        new_calculations = ["add 3 3 = 6"]
        for calc in new_calculations:
            self.history.add_calculation(calc)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            expected_message = f"History successfully saved to {self.history_file}."
            self.assertIn(expected_message, fake_out.getvalue())

        df = pd.read_csv(self.history_file, dtype=str, encoding='utf-8')
        self.assertEqual(
            df['calculations'].tolist(),
            new_calculations,
            "Saving should overwrite the existing CSV file with new history."
        )

    def test_load_partial_history(self) -> None:
        """Test loading a history when the CSV file contains additional irrelevant columns."""
        calculations = ["add 4 5 = 9", "subtract 9 2 = 7"]
        df = pd.DataFrame({
            'calculations': calculations,
            'timestamp': ["2024-01-01", "2024-01-02"]
        })
        df.to_csv(self.history_file, index=False, encoding='utf-8')

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            expected_message = f"History successfully loaded from {self.history_file}."
            self.assertIn(expected_message, fake_out.getvalue())

        self.assertEqual(
            self.history.get_history(),
            calculations,
            "Only 'calculations' should be loaded, ignoring other columns."
        )

    def test_save_load_unicode_characters(self) -> None:
        """Test saving and loading history with Unicode characters."""
        calculations = [
            "add 𝟚 𝟛 = 𝟝",
            "multiply π 𝟜 = 𝟙𝟢"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            expected_save_message = f"History successfully saved to {self.history_file}."
            self.assertIn(expected_save_message, fake_out.getvalue())

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            expected_load_message = f"History successfully loaded from {self.history_file}."
            self.assertIn(expected_load_message, fake_out.getvalue())

        self.assertEqual(
            self.history.get_history(),
            calculations,
            "Loaded history with Unicode characters does not match the original."
        )

    def test_save_history_with_special_characters(self) -> None:
        """Test saving history entries that contain special characters."""
        calculations = [
            "add 2+2=4",
            "subtract 5-3=2",
            "multiply 4*5=20",
            "divide 10/2=5"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            expected_message = f"History successfully saved to {self.history_file}."
            self.assertIn(expected_message, fake_out.getvalue())

        df = pd.read_csv(self.history_file, dtype=str, encoding='utf-8')
        self.assertEqual(
            df['calculations'].tolist(),
            calculations,
            "Saved calculations with special characters do not match the history."
        )


if __name__ == '__main__':
    unittest.main()
