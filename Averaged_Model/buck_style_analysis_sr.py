from utils_pkg import *

if __name__=="__main__":

    output_file = open_loop_output_file
    output_pickle_file = open_loop_output_pickle_file

    parser = argparse.ArgumentParser(description="Process a Buck Style Converter")
    parser.add_argument("-ga", required=True, type=str2bool, help="General analysis of impedance blocks requested.")
    parser.add_argument("-pa", required=True, type=str2bool, help="Parameter analysis of impedance blocks requested.")
    parser.add_argument("-p", required=True, help="Path at which analysis is requested")

    args = vars(parser.parse_args())

    #Conduct general analysis if it is requested.
    if args["ga"]:

        #Create path to output results of analysis.
        output_path = os.path.join(os.path.dirname(__file__), args["p"])

        #Get circuit parameters of requested
        parameters = find_circuit_params(args["p"], "General", "Open")
        converter_name = parameters.pop("Name")

        Ron1 = parameters["Ron1"]
        Ron2 = parameters["Ron2"]
        RL1 = parameters["RL1"]
        L1 = parameters["L1"]
        Rload = parameters["Rload"]
        RC1 = parameters["RC1"]
        C1 = parameters["C1"]

        if not converter_name:
            print("Please specify a name for the converter in parameter file to begin analysis.")
            sys.exit(1)

        print("{} Analysis...".format(converter_name))
        print("\n")

        s = sympy.symbols("s")

        load_stage = parallel(Rload, addStr(RC1, C1))

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
        v1_control_output = minStr(Vin, multStr(primary_current, addStr(Ron1, induct_stage_primary)))
        v1_primary_current = divStr(divStr(v1_control_output, multStr(duty_cycle, inv_duty_cycle)), primary_impedance)
        v1_secondary_current = multStr(v1_primary_current, divStr("1", n_coeff))
        v1_output_voltage = multStr(secondary_current, "-1", load_stage)

        duty_output_transfer = divStr(v1_output_voltage, duty_cycle)

        duty_output_transfer = sympy.simplify(duty_output_transfer)

        transfer_functions = {input_to_output_string: input_output_transfer,
                                input_impedance_string: input_impedance_transfer,
                                output_impedance_string: output_impedance_transfer,
                                control_to_output_string: duty_output_transfer}
        
        print_transfers(transfer_functions, os.path.join(output_path, output_file))

        pickle_transfers(transfer_functions, os.path.join(output_path, output_pickle_file))

    #Conduct parameter analysis if it is requested at the command line.
    if args["pa"]:
        params = {}

        components = find_circuit_params(args["p"], "Parameter", "Open")
        params["Vout"] = components.pop("Vout")
        params["Vin"] = components.pop("Vin")

        #If general analysis was already conducted, transfer functions will be in working session,
        #else we need to import them from our previously conducted analysis.
        if not args["ga"]:
            transfer_functions = load_pickled_transfers(args["p"], "Open")

            #Convert transfer functions that are currently type string to sympy variables to be 
            #used for analysis.
            for transfer_name, transfer in transfer_functions.items():
                transfer_functions[transfer_name] = sympy.simplify(transfer)
    
        #Calculate duty cycle for converter.
        all_values = {**components, **params}
        duty_cycle_expr = str(calculate_duty_cycle(transfer_functions["Input to Output Transfer Function"], 0))

        duty_cycle_value = evaluate_expression(substitute_expression(duty_cycle_expr, all_values), True)
        print("Duty Cycle Value is {:.3}".format(duty_cycle_value))
        all_values.update({"D": duty_cycle_value})

        graph_transfers(transfer_functions, all_values)