
from app.operations.addition import add
from app.operations.division import div
from app.operations.multiplication import multi
from app.operations.subtraction import sub
from app.operations.exponent import expo
from app.operations.modulus import mod

def addition(a: float, b: float) -> float:
    return add(a,b)  # This is the actual math part: we add the two numbers together and return the result.

def subtraction(a: float, b: float) -> float:
    
    return sub(a,b)# This subtracts the second number (b) from the first number (a) and returns the result.

def multiplication(a: float, b: float) -> float:
    
    return multi(a,b) # This multiplies the two numbers and returns the result.

def exponent(a:float, b:float)-> float:
    return expo(a,b)

def modulus(a:float, b:float)-> float:
    return mod(a,b)

def division(a: float, b: float) -> float:
    
    return div(a,b)
"""
def exponent(a: float, b: float) -> float:
    return 

    """