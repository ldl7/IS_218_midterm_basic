# calculator.py

import logging
from app.operations import addition, subtraction, multiplication, division, exponent, modulus
from app.history import History
from dotenv import load_dotenv
import os

load_dotenv()

# Configure logging
logging.basicConfig(
    filename=os.getenv("LOG_FILE", "default.log"),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def calculator(inputs=None):
    """
    Interactive calculator that supports basic arithmetic operations
    and manages calculation history with save and load functionalities.
    
    :param inputs: Optional parameter for automated inputs (not used in this implementation).
    """
    
    history = History()
    history_file = 'history.csv'

    logging.info("Calculator started.")
    print("Welcome to the Calculator!")
    print("Available operations: add, sub, multi, div, expo, mod")
    print("Available commands: history, clear, undo, save, load, help, exit")
    print("Format is <operation> <number1> <number2>")

    while True:
        user_input = input("Enter an operation (add, sub, multi, div) and two numbers, or a command: ").strip()

        if not user_input:
            print("No input detected. Please enter a valid command or operation.")
            logging.warning("No input detected.")
            continue

        command = user_input.lower()

        if command == "exit":
            logging.info("Exiting calculator.")
            print("Exiting calculator...")
            break
        elif command == "history":
            logging.info("History retrieved.")
            print("Calculation History:")
            for calc in history.get_history():
                print(calc)
            continue
        elif command == "clear":
            history.clear_history()
            logging.info("History cleared.")
            print("History Cleared.")
            continue
        elif command == "undo":
            history.undo_last()
            logging.info("Last calculation undone.")
            print("Last calculation undone.")
            continue
        elif command == "save":
            history.save(history_file)
            logging.info("History saved to file.")
            continue
        elif command == "load":
            try:
                history.load(history_file)
                print("History successfully loaded.")
                continue
            except FileNotFoundError:
                logging.error("File not found during history load.")
                print("File was not found.")
                continue
        elif command == "help":
            print("History Features: undo, clear, history, save, load.")
            print("Math Functions: add, sub, multi, div, expo, mod.")
            continue
        else:
            try:
                operation, num1, num2 = user_input.split()
                num1 = float(num1)
                num2 = float(num2)
            except ValueError:
                logging.warning("Invalid input format detected.")
                print("Invalid input. Please follow the format: <operation> <num1> <num2>.")
                continue

            try:
                if operation == "add":
                    result = addition(num1, num2)
                elif operation == "sub":
                    result = subtraction(num1, num2)
                elif operation == "multi":
                    result = multiplication(num1, num2)
                elif operation == "div":
                    result = division(num1, num2)
                elif operation == "expo":
                    result = exponent(num1, num2)
                elif operation == "mod":
                    result = modulus(num1, num2)
                else:
                    logging.warning("Unknown operation detected.")
                    print("Unknown operation. Supported operations: add, subtract, multiply, divide, exponent, modulus.")
                    continue

                calculation_str = f"{operation} {num1} {num2} = {result}"
                history.add_calculation(calculation_str)
                logging.info("Calculation performed: %s", calculation_str)
                print(f"Result: {result}")
            except ValueError as error:
                logging.error("Error during calculation: Divide by zero not allowed")
                print(error)

def main():
    """
    Main loop of the calculator application for interactive use.
    """
    calculator()

if __name__ == "__main__":
    main()
