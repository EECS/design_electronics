from utils_pkg import *

if __name__=="__main__":
    print("ANALYZING A TYPE I COMPENSATOR...")
    print("\n")
    
    general_analysis_path = "Type_I/analysis.txt"
    general_analysis_file = open(general_analysis_path, "w")

    parser = argparse.ArgumentParser(description="Process a Type I compensator")
    parser.add_argument("-r1", required=False, help="R1 resistor in Type I compensator in kOhms")

    args = vars(parser.parse_args())

    components = {}
    transfer_functions = {}

    components["R21"] = float(args["r1"])*1000
    components["C21"] = float(args["c1"])*1e-9

    output_error_transfer = divStr("-1", multStr("s", "R21", "C21"))
    output_error_transfer = sympy.simplify(output_error_transfer)

    transfer_functions["Output Voltage to Error Voltage Transfer Function"] = output_error_transfer

    graph_transfers(transfer_functions, components)

    pickle.dump(output_error_transfer, general_analysis_file)
    general_analysis_file.close()
