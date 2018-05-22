import math, re, cmath
import matplotlib.pyplot as plt
import numpy

def js_math(transfer_function):
    num_points = 10000

    start_frequency = 1 #Hz
    end_frequency = 101 #kHz
    step_size = int(((end_frequency*1000)-start_frequency)/num_points)

    bode_x_range = [step for step in range(start_frequency, end_frequency*1000, step_size)]

    #Define circuit parameters to graph
    vals = {"R1": '1000', "R2":'10000'}
    #Replace symbols with values defined in vals dictionary
    for k, v in vals.items():
        #Find key and only the key. Example, finds R1 and not R11 by separating on the non-word boundary.
        transfer_function = re.sub(r"\b"+k+r"\b", v, transfer_function)

    denom_start = transfer_function.find("/")

    if denom_start != -1:
        numerator = transfer_function[:denom_start]
        denominator = transfer_function[denom_start+1:]
    
    print(transfer_function)

    phases = []
    mags = []

    for f in bode_x_range:
        complex_replace = str(2j*cmath.pi*f)

        if denom_start != -1:
            num = numerator.replace("s", complex_replace)
            c_num = complex(eval(num))
            denom = denominator.replace("s", complex_replace)
            c_denom = complex(eval(denom))
            c_transfer = c_num*c_denom/(c_denom*c_denom)
        else:
            c_transfer = complex(transfer_function.replace("s", complex_replace))

        mags.append(20*math.log10(abs(c_transfer)))
        phases.append(cmath.phase(c_transfer)*180/cmath.pi)

    #Find and print -3dB point if in list of analyzed frequencies
    print(next((bode_x_range[mags.index(i)] for i in mags if i <= -3), 'Increase Frequency Range to see -3 dB point of Transfer Function'))
    #Find and print cross over frequency if in list of analyzed frequencies
    print(next((bode_x_range[phases.index(i)] for i in phases if i <= 0), 'Increase frequency range to see cross over frequency of transfer function'))

    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    ax1.set_xscale("log")
    ax2.set_xscale("log")
    ax1.plot(bode_x_range, mags)
    ax2.plot(bode_x_range, phases)
    plt.show()

    return bode_x_range

transfer = "(R1)/(R1+R2)"
js_math(transfer)