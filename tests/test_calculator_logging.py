"""tests/test_calculator_logging.py

Unit tests for the calculator's logging functionality.
"""

import unittest
from unittest.mock import patch, MagicMock

from app.calculator import calculator


class TestCalculatorLogging(unittest.TestCase):
    """Unit tests for calculator logging functionality."""

    @patch('builtins.input', side_effect=['add 2 3', 'exit'])
    @patch('logging.info')
    def test_calculator_start_logging(
        self, mock_logging_info: MagicMock, _mock_input: MagicMock
    ) -> None:
        """
        Test that the calculator start log message is recorded.
        """
        calculator()
        mock_logging_info.assert_any_call("Calculator started.")

    @patch('builtins.input', side_effect=['exit'])
    @patch('logging.info')
    def test_calculator_exit_logging(
        self, mock_logging_info: MagicMock, _mock_input: MagicMock
    ) -> None:
        """
        Test that the calculator exit log message is recorded.
        """
        calculator()
        mock_logging_info.assert_any_call("Exiting calculator.")

    @patch('builtins.input', side_effect=['history', 'exit'])
    @patch('logging.info')
    def test_history_logging(
        self, mock_logging_info: MagicMock, _mock_input: MagicMock
    ) -> None:
        """
        Test that the history retrieval log message is recorded when history is accessed.
        """
        calculator()
        mock_logging_info.assert_any_call("History retrieved.")

    @patch('builtins.input', side_effect=['clear', 'exit'])
    @patch('logging.info')
    def test_clear_history_logging(
        self, mock_logging_info: MagicMock, _mock_input: MagicMock
    ) -> None:
        """
        Test that the clear history log message is recorded.
        """
        calculator()
        mock_logging_info.assert_any_call("History cleared.")

    @patch('builtins.input', side_effect=['undo', 'exit'])
    @patch('logging.info')
    def test_undo_logging(
        self, mock_logging_info: MagicMock, _mock_input: MagicMock
    ) -> None:
        """
        Test that the undo log message is recorded when undo is called.
        """
        calculator()
        mock_logging_info.assert_any_call("Last calculation undone.")

    @patch('builtins.input', side_effect=['save', 'exit'])
    @patch('logging.info')
    def test_save_logging(
        self, mock_logging_info: MagicMock, _mock_input: MagicMock
    ) -> None:
        """
        Test that the save log message is recorded when history is saved.
        """
        calculator()
        mock_logging_info.assert_any_call("History saved to file.")


if __name__ == '__main__':
    unittest.main()
