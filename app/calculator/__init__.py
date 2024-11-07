from app.operations import addition 
from app.operations import subtraction
from app.operations import  multiplication
from app.operations import division
from app.history import History

def calculator(inputs=None):

    history = History()
    
    print("Welcome to the Calculator!")
    print("Available operations: add, subtract, multiply, divide")
    print("Available commands: history, clear, undo, help, exit")
    print("Format is <operation> <number1>> <number2>")

    while True:
        user_input = input("Enter an operation (add, subtract, multiply, divide) and two numbers, or a command: ")

        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break
        elif user_input.lower() == "history":
            print("Calculation History:")
            for calc in history.get_history():
                print(calc)
            continue
        elif user_input.lower() == "clear":
            history.clear_history()
            print("History Cleared.")
            continue
        elif user_input.lower() == "undo":
            history.undo_last()
            print("Last calculation undone.")
            continue
        elif user_input == "help":
            print("History Features: undo, clear, history. Math Functions: add, subtract, multiply, divide.")
        else:
            try:
                operation, num1, num2 = user_input.split()
                num1, num2 = float(num1), float(num2)
            except ValueError:
                print("Invalid input. Please follow the format: <operation> <num1> <num2>. Supported operations: add, subtract, multiply, divide.")
                continue

            if operation == "add":
                result = addition(num1, num2)
            elif operation == "subtract":
                result = subtraction(num1, num2)
            elif operation == "multiply":
                result = multiplication(num1, num2)
            elif operation == "divide":
                try:
                    result = division(num1, num2)
                except ValueError as e:
                    print(e)
                    continue
            else:
                print(f"Unknown operation. Supported operations: add, subtract, multiply, divide.")
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