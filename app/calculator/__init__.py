# calculator.py

from app.operations import addition
from app.operations import subtraction
from app.operations import multiplication
from app.operations import division
from app.operations import exponent
from app.operations import modulus
from app.history import History


def calculator(inputs=None):
    """
    Interactive calculator that supports basic arithmetic operations
    and manages calculation history with save and load functionalities.
    
    :param inputs: Optional parameter for automated inputs (not used in this implementation).
    """
    
    history = History()
    history_file = 'history.csv'

    print("Welcome to the Calculator!")
    print("Available operations: add, subtract, multiply, divide")
    print("Available commands: history, clear, undo, save, load, help, save, load, exit")
    print("Format is <operation> <number1> <number2>")

    while True:
        user_input = input("Enter an operation (add, subtract, multiply, divide) and two numbers, or a command: ").strip()

        if not user_input:
            print("No input detected. Please enter a valid command or operation.")
            continue

        command = user_input.lower()

        if command == "exit":
            print("Exiting calculator...")
            break
        elif command == "history":
            print("Calculation History:")
            for calc in history.get_history():
                print(calc)
            continue
        elif command == "clear":
            history.clear_history()
            print("History Cleared.")
            continue
        elif command == "undo":
            history.undo_last()
            print("Last calculation undone.")
            continue
        elif command == "save":
            history.save(history_file)
            continue
        elif command == "load":
            try:
                history.load(history_file)
                print("History successfully loaded.")
                print()
                continue
            except FileNotFoundError:
                print(f"File was not found.")

        elif command == "help":
            print("History Features: undo, clear, history, save, load.")
            print("Math Functions: add, subtract, multiply, divide.")
            continue
        else:
            try:
                operation, num1, num2 = user_input.split()
                num1 = float(num1)
                num2 = float(num2)
            except ValueError:
                print("Invalid input. Please follow the format: <operation> <num1> <num2>.")
                print("Supported operations: add, subtract, multiply, divide, help.")
                continue

            if operation == "add":
                result = addition(num1, num2)
            elif operation == "subtract":
                result = subtraction(num1, num2)
            elif operation == "multiply":
                result = multiplication(num1, num2)
            elif operation == "exponent":
                result = exponent(num1, num2)
            elif operation == "modulus":
                result = modulus(num1, num2)
            elif operation == "divide":
                try:
                    result = division(num1, num2)
                except ValueError as e:
                    print(e)
                    continue
            else:
                print(f"Unknown operation. Supported operations: add, subtract, multiply, divide, help.")
                continue

            calculation_str = f"{operation} {num1} {num2} = {result}"
            history.add_calculation(calculation_str)
            print(f"Result: {result}")


def main():
    """
    Main loop of the calculator application for interactive use.
    """
    calculator()


if __name__ == "__main__":
    main()
