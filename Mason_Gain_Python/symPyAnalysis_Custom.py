import sympy
from sympy.utilities.lambdify import lambdify
import pickle
import numpy

#expr_ripple_current = "(((Vin-Vo)*((Vin/Vo)*(1/Fs)))/(L1))"
#expr_ripple_voltage = expr_ripple_current+"/"+"(Fs*8*RipVo)"
#print(expr_ripple_voltage)
#standardForm = sympy.simplify(expr_ripple_voltage)

expr_transfer_vin_efficiency = "(Vo/Vin)*(Vo/Io)/((Vo/Vin)*RQ1 + RL1 + (Vo/Io))" 
expr_transfer_vd_efficiency = "-(Vo/Io)*((Vo/Vin) - 1)/((Vo/Vin)*RQ1 + RL1 + (Vo/Io))"
expr_transfer_iin_efficiency = "Vo**2/(Io*RL1*Vin + Io*RQ1*Vo + Vin*Vo)"
efficiency = "(("+expr_transfer_vin_efficiency+")*"+"(VD1/Vin)*"+"("+expr_transfer_vd_efficiency+"))"+"*("+expr_transfer_iin_efficiency+")"
print(efficiency)
#standardForm = sympy.simplify(efficiency)

#expr = "((Vin-Vo)/L)*(Vo/Vin)*(1/Fs)" 
#print(expr)
standardForm = sympy.simplify(efficiency)

print("Standard form of Equation: "+ str(standardForm))