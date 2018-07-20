import sympy
from sympy.utilities.lambdify import lambdify
import pickle
import numpy

expr = "((Vin-Vo)*((Vin/Vo)*(1/Fs)))/(RipIo)"
standardForm = sympy.simplify(expr)

print("Standard form of Equation: "+ str(standardForm))