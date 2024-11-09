# app/history/__init__.py

import logging
import pandas as pd
import os 
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class History:
    """
    Class to manage the history of calculations.
    """
    def __init__(self):
        # Initialize an empty list to store calculations.
        self.history = []
        logging.debug("Initialized History instance.")

    def add_calculation(self, calculation: str):
        """
        Adds a calculation to the history.
        :param calculation: String representation of the calculation.
        """
        if not isinstance(calculation, str):
            raise TypeError("Calculation must be a string.")
        self.history.append(calculation)
        logging.debug(f"Added calculation: {calculation}")

    def clear_history(self):
        """
        Clears all calculations from the history.
        """
        self.history.clear()
        logging.debug("Cleared all history.")

    def undo_last(self):
        """
        Removes the last calculation from the history.
        """
        if self.history:
            removed = self.history.pop()
            logging.debug(f"Removed last calculation: {removed}")
        else:
            logging.warning("Attempted to undo, but history is already empty.")
            print("History is already empty.")

    def get_history(self):
        """
        Retrieves a copy of the list of calculations.
        :return: List of calculations.
        """
        logging.debug("Retrieved history.")
        return self.history.copy()

    def save(self, file_path: str = None):
        """
        Saves the history to a CSV file.

        :param file_path: Path to the CSV file where history will be saved.
                          Defaults to the value of HISTORY_FILE environment variable or 'default.csv'.
        """
        if file_path is None:
            # Retrieve from environment variable with a fallback
            file_path = os.getenv("HISTORY_FILE", "default.csv")
            logging.debug(f"No file_path provided. Using HISTORY_FILE from env: {file_path}")
        df = pd.DataFrame({'calculations': self.history})
        df.to_csv(file_path, index=False)
        logging.info(f"History successfully saved to {file_path}.")
        print(f"History successfully saved to {file_path}.")

    def load(self, file_path: str = None):
        """
        Loads the history from a CSV file.

        :param file_path: Path to the CSV file from which history will be loaded.
                          Defaults to the value of HISTORY_FILE environment variable or 'default.csv'.
        """
        if file_path is None:
            # Retrieve from environment variable with a fallback
            file_path = os.getenv("HISTORY_FILE", "default.csv")
            logging.debug(f"No file_path provided. Using HISTORY_FILE from env: {file_path}")
        try:
            df = pd.read_csv(file_path)
            if 'calculations' in df.columns:
                self.history = df['calculations'].dropna().tolist()
                logging.info(f"History successfully loaded from {file_path}.")
                print(f"History successfully loaded from {file_path}.")
            else:
                logging.warning(f"'calculations' column not found in {file_path}.")
                print(f"The file {file_path} does not contain 'calculations' column.")
        except FileNotFoundError:
            logging.error(f"The file {file_path} was not found.")
            print(f"The file {file_path} was not found.")
        except pd.errors.EmptyDataError:
            logging.error(f"The file {file_path} is empty.")
            print(f"The file {file_path} is empty.")

    def get_history_with_logging(self):
        """
        Retrieve history with logging for access tracking.
        """
        logging.info("History accessed.")
        return self.get_history()
