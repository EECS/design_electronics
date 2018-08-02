import sympy
from sympy.utilities.lambdify import lambdify
import pickle
import numpy

def divStr(a, b):
    '''
    Returns a/b as string.
    '''
    return "(("+str(a)+")/("+str(b)+"))"

def minStr(a, b):
    '''
    Returns a-b as string.
    '''
    return "(("+str(a)+")-("+str(b)+"))"

def addStr(a, b):
    '''
    Returns a+b as string.
    '''
    return "(("+str(a)+")+("+str(b)+"))"

def multStr(a, b):
    '''
    Returns a*b as string.
    '''
    return "(("+str(a)+")*("+str(b)+"))"

D = sympy.symbols("D")

#expr_transfer = "((D*(Vin+VD)-VD)*Rload)/(Rload+RL1+D*RQ1)-Vo" 
#solved = sympy.solvers.solve(expr_transfer, D)
expr_transfer = "1-((VD1*(Vo-Vin))/(Vin*(VD1+Vo)))" 
solved = sympy.simplify(expr_transfer)
print(solved)

#expr = "((Vin-Vo)/L)*(Vo/Vin)*(1/Fs)" 
#print(expr)
#standardForm = sympy.simplify(efficiency)

#print("Standard form of Equation: "+ str(standardForm))