from utils_pkg import *

if __name__=="__main__":
    print("ANALYZING A TYPE I COMPENSATOR...")
    print("\n")
    
    general_analysis_path = "Type_I/analysis.txt"
    general_analysis_file = open(general_analysis_path, "wb")

    parser = argparse.ArgumentParser(description="Process a Type I compensator")
    parser.add_argument("-g", required=True, type=str2bool, help="Graph an example Type I transfer function.")

    args = vars(parser.parse_args())

    output_error_transfer = divStr("-1", multStr("s", "R21", "C21"))
    output_error_transfer = sympy.simplify(output_error_transfer)

    if args["g"]:
        components = {}
        transfer_functions = {}

        components["R21"] = 10*1000
        components["C21"] = 100*1e-9

        transfer_functions["Output Voltage to Error Voltage Transfer Function"] = output_error_transfer

        graph_transfers(transfer_functions, components)

    pickle.dump(output_error_transfer, general_analysis_file)
    general_analysis_file.close()

    print("Type I analysis complete, can be found at /{}.".format(general_analysis_path))
