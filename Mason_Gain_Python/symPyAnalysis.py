import sympy
from sympy.utilities.lambdify import lambdify
import pickle
import numpy

infile = "Test.pickle"
outfile = "standardForm.pickle"

s = sympy.symbols("s")
expr = pickle.load(open(infile, 'rb'))
standardForm = sympy.simplify(expr)

#Create expression to evaluate standard form equation quickly.
standardLambda = lambdify(s, standardForm)

with open(outfile, 'wb') as f:
    pickle.dump("\n", f)
    pickle.dump(str(standardForm), f)

print("Standard form of Equation: "+ str(standardForm))
print("DC Value of Standard Form Equation: " + str(standardLambda(0)))