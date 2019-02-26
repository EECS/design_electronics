from utils_pkg import *

if __name__=="__main__":
    print("ANALYZING A BUCK BOOST STYLE CONVERTER...")
    print("\n")

    Ron1 = "(Ron/D)"
    Ron2 = "(Ron/(1-D))"
    RL1 = "RL1"
    L1 = "s*L1"
    Rload = "Rload"
    RC1 = "RC1"
    C1 = "(1/(s*C1))"

    Vin = "Vin"
    Vout = "Vout"

    components = {"Ron":10e-3, "RL1": 10e-3, "L1": 25e-6, "Rload": 0.63, RC1: 10e-3, "C1": 612e-6, "D": 0.612}
    params = {Vin: 20, Vout: 31.5}

    load_stage = parallel(Rload, addStr(RC1, C1))

    s = sympy.symbols("s")

    #Input to output transfer function and input impedance transfer function equations
    duty_cycle = "(D)"
    inv_duty_cycle = "(1-D)"
    induct_pri_imped_ref_coeff = "(1/(D^2))"
    n_coeff = "(D/(1-D))"

    induct_stage = addStr(RL1, L1)
    induct_stage_primary = multStr(induct_stage, induct_pri_imped_ref_coeff)

    #Impedance of the entire converter reflected to the primary
    primary_impedance = addStr(Ron1, induct_stage_primary, multStr(Ron2, divStr("1", squared(n_coeff))), multStr(load_stage, divStr("1", squared(n_coeff))))

    primary_current = divStr(Vin, primary_impedance)
    secondary_current = multStr(primary_current, divStr("1", n_coeff))

    #Secondary current is the opposite sign of primary current
    output_voltage = multStr(secondary_current, "-1", load_stage)

    input_output_transfer = divStr(output_voltage, Vin)
    input_impedance_transfer = divStr(Vin, primary_current)

    input_output_transfer = sympy.simplify(input_output_transfer)
    input_impedance_transfer = sympy.simplify(input_impedance_transfer)

    #Output impedance transfer function
    output_impedance_transfer = parallel(load_stage, addStr(multStr(addStr(Ron1, induct_stage_primary), squared(n_coeff)), Ron2))
    output_impedance_transfer = sympy.simplify(output_impedance_transfer)

    #Control to output transfer function
    secondary_current_vout = divStr(Vout, addStr(Ron2, multStr(squared(n_coeff), addStr(Ron1, induct_stage_primary))))
    v2_vout = minStr(multStr(secondary_current_vout, Ron2), Vout)
    v1_vout = divStr(multStr("-1", v2_vout), n_coeff)

    #Same equation as primary current with vin contribution, different voltage source
    primary_current_vout = divStr(divStr(v1_vout, multStr(duty_cycle, inv_duty_cycle)), primary_impedance)
    secondary_current_vout = multStr(primary_current_vout, divStr("1", n_coeff))
    output_voltage_vout = multStr(secondary_current_vout, "-1", load_stage)
    duty_output_transfer = divStr(output_voltage_vout, Vout)

    duty_output_transfer = sympy.simplify(duty_output_transfer)

    transfer_functions = {"Input to Output Transfer Function": input_output_transfer,
                            "Input Impedance Transfer Function": input_impedance_transfer,
                            "Output Impedance Transfer Function": output_impedance_transfer,
                            "Control to Output Transfer Function": duty_output_transfer}

    duty_cycle_value = calculate_duty_cycle(input_output_transfer)
    #print_transfers(transfer_functions)
    
    #graph_transfers(transfer_functions=transfer_functions, components=components)
