from sympy.utilities.lambdify import lambdify
import math, re, cmath
import matplotlib.pyplot as plt
import sympy

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

def print_transfers(transfer_functions):
    '''
    Prints transfer functions of converter.
    '''
    s = sympy.symbols("s")

    for transfer_name, transfer in transfer_functions.items():
        print("{}:".format(transfer_name))
        print(transfer)    
        print("DC Value of {}:".format(transfer_name))
        print(lambdify(s, transfer)(0))
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
    universal_params = {"sqrt": "math.sqrt"}

    for k, v in values.items():
        function = re.sub(r"\b{}\b".format(k), "({})".format(str(v)), function)
    
    for k, v in universal_params.items():
        function = re.sub(r"\b{}\b".format(k), str(v), function)
    
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

def graph_transfers(transfer_functions, components):
    '''
    Prints transfer functions of converter.
    '''
    start_frequency = 1 #Hz
    end_frequency = 100 #kHz
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

        ax2 = plt.subplot(2,len(transfer_functions),plot_idx+4)
        ax2.set_xscale("log")
        ax2.plot(bode_x_range, phases)
        plt.ylabel("Phase (degrees)")
        plt.xlabel("Frequency (Hz)")
        plt.title("{}".format(transfer_name))

        plot_idx += 1

    plt.show()