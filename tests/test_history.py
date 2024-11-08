# tests/test_history.py

import pytest
import unittest
import tempfile
import os
import pandas as pd
from unittest.mock import patch
from io import StringIO
from app.history import History

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
# tests/test_history.py

class TestHistory(unittest.TestCase):
    """
    Test cases for the History class's save and load methods.
    """

    def setUp(self):
        """
        Set up a temporary directory for test files.
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.history_file = os.path.join(self.temp_dir.name, 'history.csv')
        self.history = History()

    def tearDown(self):
        """
        Clean up the temporary directory after tests.
        """
        self.temp_dir.cleanup()

    def test_save_history_with_entries(self):
        """
        Test saving a history with multiple calculations to a CSV file.
        """
        # Add calculations to history
        calculations = [
            "add 2 3 = 5",
            "subtract 10 4 = 6",
            "multiply 3 7 = 21"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        # Save history to CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            self.assertIn(f"History successfully saved to {self.history_file}.", fake_out.getvalue())

        # Read the CSV file using pandas
        df = pd.read_csv(self.history_file, dtype=str)

        # Verify the contents
        self.assertIn('calculations', df.columns, "CSV does not contain 'calculations' column.")
        self.assertEqual(df['calculations'].tolist(), calculations, "Saved calculations do not match the history.")

    def test_save_empty_history(self):
        """
        Test saving an empty history to a CSV file.
        """
        # Ensure history is empty
        self.assertEqual(len(self.history.get_history()), 0, "History is not empty.")

        # Save history to CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            self.assertIn(f"History successfully saved to {self.history_file}.", fake_out.getvalue())

        # Read the CSV file using pandas
        df = pd.read_csv(self.history_file, dtype=str)

        # Verify the contents
        self.assertIn('calculations', df.columns, "CSV does not contain 'calculations' column.")
        self.assertEqual(len(df), 0, "CSV file should be empty for empty history.")

    def test_load_history_with_entries(self):
        """
        Test loading a history from a CSV file with multiple calculations.
        """
        # Prepare a CSV file with calculations
        calculations = [
            "add 2 3 = 5",
            "subtract 10 4 = 6",
            "multiply 3 7 = 21"
        ]
        df = pd.DataFrame({'calculations': calculations})
        df.to_csv(self.history_file, index=False)

        # Load history from CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            self.assertIn(f"History successfully loaded from {self.history_file}.", fake_out.getvalue())

        # Verify the history
        self.assertEqual(self.history.get_history(), calculations, "Loaded history does not match the CSV file.")

    def test_load_empty_history_file(self):
        """
        Test loading from an empty CSV file.
        """
        # Create an empty CSV file
        open(self.history_file, 'w').close()

        # Load history from CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            output = fake_out.getvalue()

        # Verify the printed message
        self.assertIn(f"The file {self.history_file} is empty.", output)

        # Verify that history is still empty
        self.assertEqual(len(self.history.get_history()), 0, "History should remain empty after loading from an empty file.")

    def test_load_nonexistent_file(self):
        """
        Test loading history from a non-existent CSV file.
        """
        # Define a non-existent file path
        nonexistent_file = os.path.join(self.temp_dir.name, 'nonexistent.csv')

        # Ensure the file does not exist
        self.assertFalse(os.path.exists(nonexistent_file), "File unexpectedly exists.")

        # Load history from CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(nonexistent_file)
            output = fake_out.getvalue()

        # Verify the printed message
        self.assertIn(f"The file {nonexistent_file} was not found.", output)

        # Verify that history remains empty
        self.assertEqual(len(self.history.get_history()), 0, "History should remain empty when loading from a non-existent file.")

    def test_save_and_load_cycle(self):
        """
        Test saving and then loading history to ensure data persistence.
        """
        # Add calculations to history
        calculations = [
            "add 1 1 = 2",
            "divide 10 2 = 5"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        # Save history to CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            self.assertIn(f"History successfully saved to {self.history_file}.", fake_out.getvalue())

        # Create a new History instance and load from CSV
        new_history = History()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            new_history.load(self.history_file)
            self.assertIn(f"History successfully loaded from {self.history_file}.", fake_out.getvalue())

        # Verify that the new history matches the original
        self.assertEqual(new_history.get_history(), calculations, "Loaded history does not match the original history.")

    def test_save_overwrites_existing_file(self):
        """
        Test that saving history overwrites an existing CSV file.
        """
        # Create an initial CSV file with different data
        initial_calculations = ["multiply 2 2 = 4"]
        df_initial = pd.DataFrame({'calculations': initial_calculations})
        df_initial.to_csv(self.history_file, index=False)

        # Add new calculations to history
        new_calculations = ["add 3 3 = 6"]
        for calc in new_calculations:
            self.history.add_calculation(calc)

        # Save history to the same CSV file and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            self.assertIn(f"History successfully saved to {self.history_file}.", fake_out.getvalue())

        # Read the CSV file using pandas
        df = pd.read_csv(self.history_file, dtype=str)

        # Verify that the CSV now contains only the new calculations
        self.assertEqual(df['calculations'].tolist(), new_calculations, "Saving should overwrite the existing CSV file with new history.")

    def test_load_partial_history(self):
        """
        Test loading a history when the CSV file contains additional irrelevant columns.
        """
        # Prepare a CSV file with 'calculations' and other columns
        calculations = ["add 4 5 = 9", "subtract 9 2 = 7"]
        df = pd.DataFrame({
            'calculations': calculations,
            'timestamp': ["2024-01-01", "2024-01-02"]
        })
        df.to_csv(self.history_file, index=False)

        # Load history from CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            self.assertIn(f"History successfully loaded from {self.history_file}.", fake_out.getvalue())

        # Verify that only 'calculations' are loaded
        self.assertEqual(self.history.get_history(), calculations, "Only 'calculations' should be loaded, ignoring other columns.")

    def test_save_load_unicode_characters(self):
        """
        Test saving and loading history with Unicode characters.
        """
        # Add calculations with Unicode characters
        calculations = [
            "add 𝟚 𝟛 = 𝟝",
            "multiply π 𝟜 = 𝟙𝟢"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        # Save history to CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            self.assertIn(f"History successfully saved to {self.history_file}.", fake_out.getvalue())

        # Load history from CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            self.assertIn(f"History successfully loaded from {self.history_file}.", fake_out.getvalue())

        # Verify that the history matches
        self.assertEqual(self.history.get_history(), calculations, "Loaded history with Unicode characters does not match the original.")

    def test_save_history_with_special_characters(self):
        """
        Test saving history entries that contain special characters.
        """
        # Add calculations with special characters
        calculations = [
            "add 2+2=4",
            "subtract 5-3=2",
            "multiply 4*5=20",
            "divide 10/2=5"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        # Save history to CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            self.assertIn(f"History successfully saved to {self.history_file}.", fake_out.getvalue())

        # Read the CSV file using pandas
        df = pd.read_csv(self.history_file, dtype=str)

        # Verify the contents
        self.assertEqual(df['calculations'].tolist(), calculations, "Saved calculations with special characters do not match the history.")

    def test_load_history_with_nan_values(self):
        """
        Test loading history from a CSV file that contains NaN values in the 'calculations' column.
        """
        # Prepare a CSV file with NaN values
        calculations = ["add 1 2 = 3", None, "multiply 3 4 = 12", pd.NA]
        df = pd.DataFrame({'calculations': calculations})
        df.to_csv(self.history_file, index=False)

        # Load history from CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            output = fake_out.getvalue()
            self.assertIn(f"History successfully loaded from {self.history_file}.", output)

        # Expected history after dropping NaN values
        expected_history = ["add 1 2 = 3", "multiply 3 4 = 12"]

        # Verify the history
        self.assertEqual(self.history.get_history(), expected_history, "Loaded history should exclude NaN values.")

    def test_save_history_with_numeric_strings(self):
        """
        Test saving history entries that are numeric strings.
        """
        # Add calculations that are numeric strings
        calculations = [
            "123",
            "456.789",
            "-10",
            "0"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        # Save history to CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            self.assertIn(f"History successfully saved to {self.history_file}.", fake_out.getvalue())

        # Read the CSV file using pandas
        df = pd.read_csv(self.history_file, dtype=str)

        # Verify the contents
        self.assertEqual(df['calculations'].tolist(), calculations, "Saved numeric string calculations do not match the history.")

    def test_save_history_with_quotes(self):
        """
        Test saving history entries that contain quotes.
        """
        # Add calculations with quotes
        calculations = [
            'add "2" "3" = "5"',
            "subtract '10' '4' = '6'"
        ]
        for calc in calculations:
            self.history.add_calculation(calc)

        # Save history to CSV and capture logs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.history.save(self.history_file)
            self.assertIn(f"History successfully saved to {self.history_file}.", fake_out.getvalue())

        # Read the CSV file using pandas
        df = pd.read_csv(self.history_file, dtype=str)

        # Verify the contents
        self.assertEqual(df['calculations'].tolist(), calculations, "Saved calculations with quotes do not match the history.")
    def test_load_valid_file():
        """Test loading history from a valid CSV file with 'calculations' column."""
        history = History()
    
    # Create a temporary file with valid data
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            df = pd.DataFrame({"calculations": ["add 2 3 = 5", "subtract 5 1 = 4"]})
            df.to_csv(tmp_file.name, index=False)

        # Capture output and verify loading history
        with patch("sys.stdout", new=StringIO()) as fake_out:
            history.load(tmp_file.name)
            output = fake_out.getvalue()
        
        assert "History successfully loaded" in output
        assert history.get_history() == ["add 2 3 = 5", "subtract 5 1 = 4"]

        # Clean up the temporary file
        os.remove(tmp_file.name)

    def test_load_file_not_found():
        """Test loading history from a non-existent file to trigger FileNotFoundError."""
        history = History()
        non_existent_file = "non_existent_history.csv"

        with patch("sys.stdout", new=StringIO()) as fake_out:
            history.load(non_existent_file)
            output = fake_out.getvalue()
        
        assert f"The file {non_existent_file} was not found." in output
        assert history.get_history() == []

    def test_load_empty_file(self):
        """Test loading history from an empty CSV file to trigger EmptyDataError."""
        # Create an empty temporary file
        open(self.history_file, 'w').close()

        # Capture output and verify handling of empty file
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            output = fake_out.getvalue()

        self.assertIn("is empty", output)
        self.assertEqual(self.history.get_history(), [])

    def setUp(self):
        """Set up a temporary directory for test files."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.history_file = os.path.join(self.temp_dir.name, 'history.csv')
        self.history = History()

    def tearDown(self):
        """Clean up the temporary directory after tests."""
        self.temp_dir.cleanup()

    def test_load_valid_file(self):
        """Test loading history from a valid CSV file with 'calculations' column."""
        # Create a temporary file with valid data
        df = pd.DataFrame({"calculations": ["add 2 3 = 5", "subtract 5 1 = 4"]})
        df.to_csv(self.history_file, index=False)

        # Capture output and verify loading history
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            output = fake_out.getvalue()

        self.assertIn("History successfully loaded", output)
        self.assertEqual(self.history.get_history(), ["add 2 3 = 5", "subtract 5 1 = 4"])

    def test_load_file_not_found(self):
        """Test loading history from a non-existent file to trigger FileNotFoundError."""
        non_existent_file = "non_existent_history.csv"

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.history.load(non_existent_file)
            output = fake_out.getvalue()

        self.assertIn(f"The file {non_existent_file} was not found.", output)
        self.assertEqual(self.history.get_history(), [])

    def test_load_empty_file(self):
        """Test loading history from an empty CSV file to trigger EmptyDataError."""
        # Create an empty temporary file
        open(self.history_file, 'w').close()

        # Capture output and verify handling of empty file
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.history.load(self.history_file)
            output = fake_out.getvalue()

        self.assertIn("is empty", output)
        self.assertEqual(self.history.get_history(), [])

        # Clean up the temporary file
        self.assertIn("is empty", output)
        self.assertEqual(self.history.get_history(), [])

        # Clean up the temporary file
        os.remove(self.history_file)


if __name__ == '__main__':
    unittest.main()
