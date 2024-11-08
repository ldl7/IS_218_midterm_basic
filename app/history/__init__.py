# app/history/__init__.py

import pandas as pd

class History:
    """
    Class to manage the history of calculations.
    """
    def __init__(self):
        # Initialize an empty list to store calculations.
        self.history = []

    def add_calculation(self, calculation: str):
        """
        Adds a calculation to the history.
        :param calculation: String representation of the calculation.
        """
        if not isinstance(calculation, str):
            raise TypeError("Calculation must be a string.")
        self.history.append(calculation)

    def clear_history(self):
        """
        Clears all calculations from the history.
        """
        self.history.clear()

    def undo_last(self):
        """
        Removes the last calculation from the history.
        """
        if self.history:
            self.history.pop()
        else:
            print("History is already empty.")

    def get_history(self):
        """
        Retrieves a copy of the list of calculations.
        :return: List of calculations.
        """
        return self.history.copy()
    def save(self, file_path: str = 'history.csv'):
        """
        Saves the history to a CSV file.

        :param file_path: Path to the CSV file where history will be saved.
                          Defaults to 'history.csv'.
        """
        df = pd.DataFrame({'calculations': self.history})
        df.to_csv(file_path, index=False)
        print(f"History successfully saved to {file_path}.")

    def load(self, file_path: str = 'history.csv'):
        """
        Loads the history from a CSV file.

        :param file_path: Path to the CSV file from which history will be loaded.
                          Defaults to 'history.csv'.
        """
        try:
            df = pd.read_csv(file_path)
            if 'calculations' in df.columns:
                self.history = df['calculations'].dropna().tolist()
                print(f"History successfully loaded from {file_path}.")
            
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except pd.errors.EmptyDataError:
            print(f"The file {file_path} is empty.")
