import sympy
from sympy.utilities.lambdify import lambdify
import math, re, cmath
import matplotlib.pyplot as plt

if __name__ =="__main__":
    print("ANALYZING A BUCK STYLE CONVERTER...")
    print("\n")
    Ron = "(Ron/D)"
    RL1 = "RL1"
    L1 = "s*L1"
    Rload = "Rload"
    RC1 = "RC1"
    C1 = "(1/(s*C1))"
    Vin = "Vin"

    s = sympy.symbols("s")

    load_stage = parallel(Rload, addStr(RC1, C1))
    load_pri_imped_ref_coeff = "(1/(D^2))"
    load_stage_reflected = multStr(addStr(load_stage, RL1, L1), load_pri_imped_ref_coeff)
    
    pri_load_curr_ref_coeff = "(1/D)"

    #Calculate primary side current, neglecting diode's contribution (due to small signal purposes)
    primary_current = divStr(Vin, addStr(Ron, load_stage_reflected))
    load_current = multStr(primary_current, pri_load_curr_ref_coeff)
    output_voltage = multStr(load_current, load_stage)

    input_output_transfer = divStr(output_voltage, Vin)
    input_impedance_transfer = divStr(Vin, primary_current)

    input_output_transfer = sympy.simplify(input_output_transfer)
    input_impedance_transfer = sympy.simplify(input_impedance_transfer)

    print_transfers(input_output_transfer, input_impedance_transfer)

    components = {"Ron":10, "RL1": 10, "L1": 10, "Rload": 1, RC1: 10, "C1": 100, "Vin": 20}
