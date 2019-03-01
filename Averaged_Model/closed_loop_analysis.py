from utils_pkg import *

if __name__=="__main__":
    output_file = closed_loop_output_file
    output_pickle_file = closed_loop_output_pickle_file

    parser = argparse.ArgumentParser(description="Conduct a Closed Loop Analysis")
    parser.add_argument("-ga", required=True, type=str2bool, help="General analysis of impedance blocks requested.")
    parser.add_argument("-pa", required=True, type=str2bool, help="Parameter analysis of impedance blocks requested.")
    parser.add_argument("-p", required=True, help="Path at which analysis is requested")
    parser.add_argument("-t", required=True, help="Type of Compensator design to be used.")

    args = vars(parser.parse_args())

    #Create path to output results of analysis.
    output_path = os.path.join(os.path.dirname(__file__), args["p"])

    #Conduct general analysis if it is requested.
    if args["ga"]:

        closed_parameters = find_circuit_params(args["p"], "General", "Closed")
        open_loop_transfers = load_pickled_transfers(args["p"], "Open")
        H = "H"
        VM = "VM"

        if args["t"] == "1":
            output_file += typeI_error_path+".txt"
            output_pickle_file += typeI_error_path+".txt"

            R21 = closed_parameters["R21"]
            C21 = closed_parameters["C21"]
            
            #Sympy symbol returned.
            error_transfer = load_pickled_transfers(typeI_error_path, "Compensator")
        elif args["t"] == "2":
            output_file += typeII_error_path+".txt"
            output_pickle_file += typeII_error_path+".txt"
            pass
        elif args["t"] == "3":
            output_file += typeIII_error_path+".txt"
            output_pickle_file += typeIII_error_path+".txt"
            pass
        
        plant_transfer = divStr(multStr(open_loop_transfers[control_to_output_string], error_transfer, H), VM)
        plant_transfer = sympy.simplify(plant_transfer)

        closed_vref_vo_transfer = divStr(plant_transfer, multStr(H, addStr("1", plant_transfer)))
        closed_vg_vo_transfer = divStr(open_loop_transfers[input_to_output_string], addStr("1", plant_transfer))
        closed_output_impedance = divStr(multStr("-1", open_loop_transfers[output_impedance_string]), addStr("1", plant_transfer))

        closed_vref_vo_transfer = sympy.simplify(closed_vref_vo_transfer)
        closed_vg_vo_transfer = sympy.simplify(closed_vg_vo_transfer)
        closed_output_impedance = sympy.simplify(closed_output_impedance)

        closed_transfer_functions = {closed_vref_vo_string: closed_vref_vo_transfer, closed_vg_vo_string: closed_vg_vo_transfer,
                                    closed_output_impedance_string: closed_output_impedance}

        print_transfers(closed_transfer_functions, os.path.join(output_path, output_file))

        pickle_transfers(closed_transfer_functions, os.path.join(output_path, output_pickle_file))

    #Conduct parameter analysis if it is requested at the command line.
    if args["pa"]:
        params = {}

        open_components = find_circuit_params(args["p"], "Parameter", "Open")
        params["Vout"] = open_components.pop("Vout")
        params["Vin"] = open_components.pop("Vin")

        #If general analysis was already conducted, transfer functions will be in working session,
        #else we need to import them from our previously conducted analysis.
        if not args["ga"]:
            open_loop_transfers = load_pickled_transfers(args["p"], "Open")
            closed_transfer_functions = load_pickled_transfers(args["p"], "Closed")

        #Convert transfer functions that are currently type string to sympy variables to be 
        #used for analysis.
        for transfer_name, transfer in open_loop_transfers.items():
            open_loop_transfers[transfer_name] = sympy.simplify(transfer)
    
        #Calculate duty cycle for converter.
        all_values = {**open_components, **params}
        duty_cycle_expr = str(calculate_duty_cycle(open_loop_transfers[input_to_output_string], 0))

        duty_cycle_value = evaluate_expression(substitute_expression(duty_cycle_expr, all_values), True)
        print("Duty Cycle Value is {:.3}".format(duty_cycle_value))
        all_values.update({"D": duty_cycle_value})

        closed_components = find_circuit_params(args["p"], "Parameter", "Closed")
        print(closed_components)

        all_values.update(closed_components)

        graph_transfers(closed_transfer_functions, all_values)