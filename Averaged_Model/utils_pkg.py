from sympy.utilities.lambdify import lambdify
import math, re, cmath
import matplotlib.pyplot as plt
import sympy
import argparse, pickle, os, sys

#Universal strings to be used in all analyses
Vout = "Vout"
Vin = "Vin"
open_loop_output_file = "open_loop_analysis.txt"
open_loop_output_pickle_file = "open_loop_pickle.txt"
closed_loop_output_file = "closed_loop_analysis"
closed_loop_output_pickle_file = "closed_loop_pickle"
typeI_error_path = "Type_I"
typeII_error_path = "Type_II"
typeIII_error_path = "Type_III"
compensator_pickle_file = "analysis.txt"

input_to_output_string = "Input to Output Transfer Function"
input_impedance_string = "Input Impedance Transfer Function"
output_impedance_string = "Output Impedance Transfer Function"
control_to_output_string = "Control to Output Transfer Function"

closed_vref_vo_string = "Closed Loop Reference to Output Voltage Transfer Function"
closed_vg_vo_string = "Closed Loop Input Voltage to Output Voltage Transfer Function"
closed_output_impedance_string = "Closed Loop Output Impedance Transfer Function"

def load_pickled_transfers(path, analysis_type="Open", error_type = ""):
    '''
    params: path (string) - Path to pickled transfer functions file.
    file (string) - Analysis type of pickled transfer function at location.
    options - "Open", "Closed", "Compensator"
    '''
    transfer_functions = {}
    if analysis_type == "Open":
        with(open(os.path.join(path, open_loop_output_pickle_file), "rb")) as f:
            while True:
                try:
                    transfer_functions = pickle.load(f)
                except EOFError:
                    break
    elif analysis_type == "Compensator":
        with(open(os.path.join(path, compensator_pickle_file), "rb")) as f:
            while True:
                try:
                    transfer_functions = pickle.load(f)
                except EOFError:
                    break
    elif analysis_type == "Closed":
        with(open(os.path.join(path, closed_loop_output_pickle_file+error_type+".txt"), "rb")) as f:
            while True:
                try:
                    transfer_functions = pickle.load(f)
                except EOFError:
                    break

    return transfer_functions


def pickle_transfers(transfers, file):
    '''
    params: transfers (dict) - Dictionary of all
    transfer functions to pickle.
    file (string) - String of file path to pickle transfer
    functions to.
    '''
    f = open(file, "wb")
    transfers_string = {}
    for k, v in transfers.items():
        transfers_string[k] = str(v)
    
    pickle.dump(transfers_string, f)
    f.close()

def print_and_log(text, out_file=""):
    '''
    params: text (string) - Text to be printed.
    out_file(str) - Output path to write text, if wanted.
    '''
    if out_file != "":
        out = open(out_file, "a")
        out.write(str(text))
        out.write("\n")
        out.close()
    
    print(text)

def find_circuit_params(path, analysis="General", analysis_type="Open"):
    '''
    params: path (string) - A string to the path of the circuit to
    be analyzed. Assumes that the analysis file ends in "_params".
    type (string) - Type of analysis requested. Options are "General"
    and "Parameter".
    '''
    import glob

    #Open analysis file at relative path specified.
    if analysis_type == "Open":
        file_search = "*open_params.txt"
    elif analysis_type == "Closed":
        file_search = "*closed_params.txt"

    analysis_file = glob.glob(os.path.join(os.path.dirname(__file__),
        "{}\\{}".format(path, file_search)))
    
    if not analysis_file:
        print("Analysis file not found, please provide parameter file, exiting.")
        sys.exit(1)

    analysis_file = open(analysis_file[0], "r")
    parameters = {}

    #Read lines in file for general parameter analysis.
    if analysis =="General":
        begin_read = False

        for line in analysis_file.readlines():
            if begin_read:
                if "##" in line:
                    break
                else:
                    #Get parameter at line, seperated by equals sign,
                    #and strip white space from parameter.
                    line_parameters = line.split("=")
                    parameters[line_parameters[0].strip()] = line_parameters[1].strip()
            elif "#" in line:
                begin_read = True


    elif analysis == "Parameter":
        begin_read = False

        for line in analysis_file.readlines():
            if begin_read:
                #Get parameter at line, seperated by equals sign,
                #and strip white space from parameter.
                line_parameters = line.split("=")
                parameters[line_parameters[0].strip()] = line_parameters[1].strip()
            elif "##" in line:
                begin_read = True
    else:
        print("Incorrect type of analysis specified, exiting.")
        analysis_file.close()
        sys.exit(1)

    analysis_file.close()

    return parameters

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def divStr(*args):
    '''
    Returns a/b/c/etc. as string.
    '''
    ret ="("
    for arg in args:
        if ret == "(":
            ret += "({})".format(arg)
        else:
            ret += "/({})".format(arg)
    
    return ret+")"

def minStr(*args):
    '''
    Returns a+b as string.
    '''
    ret ="("
    for arg in args:
        if ret == "(":
            ret += "({})".format(arg)
        else:
            ret += "-({})".format(arg)
    
    return ret+")"

def addStr(*args):
    '''
    Returns a+b as string.
    '''
    ret ="("
    for arg in args:
        if ret == "(":
            ret += "({})".format(arg)
        else:
            ret += "+({})".format(arg)
    
    return ret+")"

def multStr(*args):
    '''
    Returns a*b*c*etc. as string.
    '''
    ret ="("
    for arg in args:
        if ret == "(":
            ret += "({})".format(arg)
        else:
            ret += "*({})".format(arg)
    
    return ret+")"

def parallel(a, b):
    '''
    Returns a||b as string.
    '''
    return "({0}*{1}/({0}+{1}))".format(a, b)

def bracket(a):
    '''
    Returns (a) as string.
    '''
    return "({})".format(a)

def squared(a):
    '''
    Returns (a^2) as string.
    '''
    return "(({})^2)".format(a)

def calculate_duty_cycle(input_output_transfer, d_idx=0):
    '''
    params: input_output_transfer (Sympy expression) - A
    sympy variable in the s-domain to be used to calculate the duty cycle.
    d_idx (int) - Index of solved duty_cycle equation to return (important for
    sqrt operations.)
    '''
    Vin = "Vin"
    Vout = "Vout"

    s = sympy.symbols("s")

    dc_duty = lambdify(s, input_output_transfer)(0)

    D = sympy.symbols("D")

    duty_cycle = minStr(divStr(Vout,Vin),dc_duty)
    duty_cycle = sympy.solve(duty_cycle, D)

    return duty_cycle[d_idx]

def print_and_log_transfers(transfer_functions, out_file=""):
    '''
    Prints transfer functions of converter.
    '''
    s = sympy.symbols("s")

    out = open(out_file, "w")
    out.close()
    for transfer_name, transfer in transfer_functions.items():
        print_and_log("{}:".format(transfer_name), out_file)
        print_and_log(transfer, out_file)    
        print_and_log("DC Value of {}:".format(transfer_name), out_file)
        dc_value = lambdify(s, transfer)(0)
        print_and_log(dc_value, out_file)

        if "Efficiency" in transfer_name:
            D = sympy.symbols("D")
            print_and_log("Solution for the duty cycle:", out_file)
            print_and_log(sympy.solve(minStr("Vo", dc_value), D), out_file)

        print_and_log("\n", out_file)

def print_transfers(transfer_functions, out_file=""):
    '''
    Prints transfer functions of converter.
    '''
    s = sympy.symbols("s")

    for transfer_name, transfer in transfer_functions.items():
        print("{}:".format(transfer_name))
        print(transfer)    
        print("DC Value of {}:".format(transfer_name))
        dc_value = lambdify(s, transfer)(0)
        print(dc_value)

        if "Efficiency" in transfer_name:
            D = sympy.symbols("D")
            print("Solution for the duty cycle:")
            print(sympy.solve(minStr("Vo", dc_value), D))

        print("\n")

def evaluate_expression(expression, real_only=True):
    '''
    params: expression (string) - Expression to be evaluated with
    values already subsituted in string.
    '''

    if real_only:
        print(expression)
        return abs(eval(expression))

    return eval(expression)

def substitute_expression(expression, values):
    '''
    params: expression (string) - An expression that needs 
    values substituted.
    values (dictionary) - A dictionary with key of the component (e.g. R1)
    and the value corresponding with the wanted quantity to substitute in the
    expression string.
    '''
    function = expression

    for k, v in values.items():
        function = re.sub(r"\b{}\b".format(k), "({})".format(str(v)), function)
    
    return function

def generate_transfer_data(transfer_function, bode_x_range):
    '''
    params: transfer_function (string) s-domain transfer function consisting of values to
    be used for evaluation.
    bode_x_range: (list) Hz values spaced by logarithmic steps to be used to generate
    phase and magnitude data.
    '''
    denom_start = transfer_function.find("/")
    mags = []
    phases = []

    #Create numerator and denominator strings of the transfer function.
    if denom_start != -1:
        numerator = transfer_function[:denom_start]
        denominator = transfer_function[denom_start+1:]
    else:
        numerator = transfer_function
        denominator = str(1)

    #Create magnitude and phase arrays for transfer function, replacing s with 
    #the angular frequency representation.
    for f in bode_x_range:
        complex_replace = str(2j*cmath.pi*f)
        complex_replace = "({})".format(complex_replace)

        if denom_start != -1:
            num = numerator.replace("s", complex_replace)
            c_num = complex(eval(num))
            denom = denominator.replace("s", complex_replace)
            c_denom = complex(eval(denom))
            c_denom_conj = c_denom.conjugate()
            c_transfer = (c_num/c_denom)*(c_denom_conj/c_denom_conj)
        else:
            c_transfer = complex(transfer_function.replace("s", complex_replace))

        mags.append(20*math.log10(abs(c_transfer)))
        phases.append(cmath.phase(c_transfer)*180/cmath.pi)
    
    return mags, phases

def generate_bode_range(start_freq, end_freq, num_points):
    log_step_size = ((math.log10(end_frequency*1000)-math.log10(start_frequency))/num_points)
    bode_x_range = [10**((i+1)*log_step_size) for i in range(num_points)]

    return bode_x_range

def graph_transfers(transfer_functions, components, end_freq=100):
    '''
    Graphs transfer functions of converter.
    components (dict)
    transfer_functions (dict)
    end_freq (int in kHz)
    '''
    start_frequency = 1 #Hz
    end_frequency = end_freq #kHz
    num_points = 5000
    log_step_size = ((math.log10(end_frequency*1000)-math.log10(start_frequency))/num_points)
    bode_x_range = [10**((i+1)*log_step_size) for i in range(num_points)]

    plot_idx = 1

    for transfer_name, transfer in transfer_functions.items():

        phases = []
        mags = []

        transfer_function = str(transfer)

        #Replace symbols with values defined in components dictionary.
        transfer_function = substitute_expression(transfer_function, components)

        mags, phases = generate_transfer_data(transfer_function, bode_x_range)
        
        #Create plots
        ax1 = plt.subplot(2,len(transfer_functions),plot_idx)
        ax1.set_xscale("log")
        ax1.plot(bode_x_range, mags)
        plt.ylabel("Magnitude (dB)")
        plt.xlabel("Frequency (Hz)")
        plt.title("{}".format(transfer_name))

        ax2 = plt.subplot(2,len(transfer_functions),plot_idx+len(transfer_functions))
        ax2.set_xscale("log")
        ax2.plot(bode_x_range, phases)
        plt.ylabel("Phase (degrees)")
        plt.xlabel("Frequency (Hz)")
        plt.title("{}".format(transfer_name))

        plot_idx += 1

    plt.show()

def create_typeII_transfer():
    #Control analysis for SMPS design, do not modify!!!!
    #Type II compensator:
    typeII = divStr(multStr(addStr("R22", "(1/(s*C21))"), "(1/(s*C23))"), addStr("R22", "(1/(s*C21))", "(1/(s*C23))"))
    
    return sympy.simplify(typeII)

def create_typeIII_transfer():
    #Control analysis for SMPS design, do not modify!!!!
    #Type III compensator:
    typeIII_num = divStr(multStr(addStr("(1/(s*Cf1))", "Rf2"), "(1/(s*Cf3))"), addStr("(1/(s*Cf1))", "Rf2", "(1/(s*Cf3))"))
    typeIII_denom = divStr(multStr(addStr("(1/(s*Cf2))", "Rf1"), "Rf1"), addStr("(1/(s*Cf2))", "Rf3", "Rf1"))
    typeIII = divStr(typeIII_num, typeIII_denom)

    return sympy.simplify(typeIII)