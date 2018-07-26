import sympy
from sympy.utilities.lambdify import lambdify
import pickle
import numpy

#expr_ripple_current = "(((Vin-Vo)*((Vin/Vo)*(1/Fs)))/(L1))"
#expr_ripple_voltage = expr_ripple_current+"/"+"(Fs*8*RipVo)"
#print(expr_ripple_voltage)
#standardForm = sympy.simplify(expr_ripple_voltage)

#expr_transfer_vin_efficiency = "(Vo/Vin)*(Vo/Io)/((Vo/Vin)*RQ1 + RL1 + (Vo/Io))" 
#expr_transfer_vd_efficiency = "-(Vo/Io)*((Vo/Vin) - 1)/((Vo/Vin)*RQ1 + RL1 + (Vo/Io))"
#efficiency = "(("+expr_transfer_vin_efficiency+")"+"/Vin)"+ "+(("+expr_transfer_vd_efficiency+")"+"/VD1)"
#print(efficiency)
#standardForm = sympy.simplify(efficiency)

expr = "((Vin-Vo)/L)*(Vo/Vin)*(1/Fs)" 
print(expr)
standardForm = sympy.simplify(expr)

print("Standard form of Equation: "+ str(standardForm))