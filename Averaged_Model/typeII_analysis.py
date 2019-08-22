from utils_pkg import *

if __name__=="__main__":
    print("ANALYZING A TYPE II COMPENSATOR...")
    print("\n")
    
    general_analysis_path = "Type_II/analysis.txt"
    general_analysis_file = open(general_analysis_path, "wb")

    parser = argparse.ArgumentParser(description="Process a Type II compensator")
    parser.add_argument("-g", required=True, type=str2bool, help="Graph an example Type II transfer function.")

    args = vars(parser.parse_args())
    
    numerator = addStr("1", multStr("s", "R22", "C21"))
    denominator = addStr(multStr("R21", "s", addStr("C21", "C23")), multStr(squared("s"), "R21", "R22", "C21", "C23")) 
    output_error_transfer = divStr(numerator, denominator)
    output_error_transfer = sympy.simplify(output_error_transfer)

    if args["g"]:
        components = {}
        transfer_functions = {}

        components["R21"] = 10*1000
        components["R22"] = 100*1e-9
        components["C21"] = 1*1000
        components["C22"] = 100*1e-9
        components["C23"] = 100*1e-9

        transfer_functions["Output Voltage to Error Voltage Transfer Function"] = output_error_transfer

        graph_transfers(transfer_functions, components)

    pickle.dump(output_error_transfer, general_analysis_file)
    general_analysis_file.close()

    print("Type II analysis complete, can be found at /{}.".format(general_analysis_path))
