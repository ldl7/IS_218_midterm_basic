# IS_218_midterm_basic


Calculator Program
This project is a Python-based calculator application designed to perform a variety of arithmetic and mathematical operations, including addition, subtraction, multiplication, division, modulus, and exponentiation. The project also incorporates logging, testing, and coverage analysis, making it suitable for production-level use and integration with CI/CD pipelines.

youtube linK: https://youtu.be/JT4eadXY_LY 

file purposes:
main.py: The main entry point for running calculator operations. This script interacts with operation modules and handles input/output.
Operation Modules: Separate files for each operation:
addition.py: Handles addition.
subtraction.py: Handles subtraction.
multiplication.py: Handles multiplication.
division.py: Handles division.
modulus.py: Handles modulus operations.
exponent.py: Handles exponentiation.
history.csv: Stores the calculation history in CSV format, enabling persistent storage of past calculations.
calculator.log: Logs all operations, errors, and system events to assist in debugging and monitoring.
__init__.py: Initialization files for defining the Python packages.
Test Suite: Multiple test files ensure the program's correctness and maintain code quality:
test_calculator.py: Verifies overall calculator functionality.
test_calculator_logging.py: Tests logging functionality.
test_history.py: Verifies history tracking features.
test_operations.py: Ensures individual operations are correctly implemented.
Virtual Environment and Coverage Report
venv: A virtual environment that isolates dependencies required by the calculator program, specified in requirements.txt.
htmlcov: Folder containing the HTML report generated from coverage tests, detailing which lines of code are tested.
Dependencies

The project dependencies are managed through requirements.txt:

plaintext
Copy code
astroid==3.2.4
coverage==7.6.1
dill==0.3.9
exceptiongroup==1.2.2
flake8==7.1.1
iniconfig==2.0.0
isort==5.13.2
mccabe==0.7.0
numpy==1.24.4
packaging==24.1
pandas==2.0.3
platformdirs==4.3.6
pluggy==1.5.0
pycodestyle==2.12.1
pyflakes==3.2.0
pylint==3.2.7
pytest==8.3.3
pytest-cov==5.0.0
pytest-cover==3.0.0
pytest-coverage==0.0
pytest-pylint==0.21.0
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2024.2
six==1.16.0
tomli==2.0.2
tomlkit==0.13.2
typing_extensions==4.12.2
tzdata==2024.2
Install dependencies with:

bash
Copy code
pip install -r requirements.txt
Usage
Run the Calculator Program:

bash
Copy code
python main.py
Run Tests: Execute the test suite with pytest:

bash
Copy code
pytest --cov=.
Generate Coverage Report: Coverage reports provide insight into tested lines:

bash
Copy code
pytest --cov=. --cov-report=html
View the HTML report in htmlcov/index.html.

Logging and History
Logging: All operations are logged in calculator.log for error tracking and auditing purposes.
History: Calculation history is saved to history.csv, making it easy to review past operations.
License
This project is licensed under the MIT License.
