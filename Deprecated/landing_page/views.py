from django.shortcuts import render
import math, re, cmath
from .models import ConverterEquation

def js_math(transfer_function):
    num_points = 1000

    start_frequency = 1 #Hz
    end_frequency = 11 #kHz
    step_size = int(((end_frequency*1000)-start_frequency)/num_points)

    bode_x_range = [step for step in range(start_frequency, end_frequency*1000, step_size)]

    #Define circuit parameters to graph
    vals = {"R1": '100', "R2":'10000'}
    #Replace symbols with values defined in vals dictionary
    for k, v in vals.items():
        #Find key and only the key. Example, finds R1 and not R11 by separating on the non-word boundary.
        transfer_function = re.sub(r"\b"+k+r"\b", v, transfer_function)

    #VERIFY THAT THIS IS TRUE FOR ALL TRANSFER FUNCTIONS.
    denom_start = transfer_function.find("/")

    #Create numerator and denominator strings of the transfer function.
    if denom_start != -1:
        numerator = transfer_function[:denom_start]
        denominator = transfer_function[denom_start+1:]
    else:
        numerator = transfer_function
        denominator = str(1)
    
    #Print transfer function for debugging purposes.
    print(transfer_function)

    phases = []
    mags = []

    #Create magnitude and phase arrays for transfer function, replacing s with 
    #the angular frequency representation.
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

    return bode_x_range, mags, phases

# Create your views here.
def index(request):
    #####################################
    #Index.html parameters
    #####################################
    show_testimonials = False
    paid_site = False
    trial_length = 14
    header_title = "Design Electronics"
    tag_break_lines = range(10)

    show_power_electronics = True
    show_ana_electronics = False
    show_dig_electronics = True

    #####################################
    #Circuit Parameters
    #####################################
    input_voltage = 24
    output_voltage = 5
    output_current = 3
    q1_on_res = 25 #milliOhms
    d1_on_volt = 0.7
    inductor_res = 5 #milliohms
    capacitor_res = 10 #milliohms
    inductance = 10 #microhenries
    capacitance = 100 #microfarads
    load_res = 1.67 #ohms

    #####################################
    #Model Parameters
    #####################################
    modelQuery = ConverterEquation.objects.filter(name="Landing Page Example")

    if len(modelQuery) > 0:
        input_output_transfer = modelQuery[0].input_output_transfer
        input_impedance = modelQuery[0].input_impedance
        output_impedance = modelQuery[0].output_impedance
        duty_output_transfer = modelQuery[0].duty_output_transfer

    #####################################
    #Bode Plot parameters
    #####################################
    bode_x_range, mags, phases = js_math(output_impedance)
    phase_min = min(phases)
    print(phase_min)
    phase_min += round(0.5*phase_min)

    phase_max = max(phases)
    phase_max += round(0.5*phase_max)

    mags_min = min(mags)
    mags_min += round(0.1*mags_min)

    mags_max = max(mags)
    mags_max += round(0.1*mags_max)

    return render(
        request,
        'index.html',
        context={'header_title': header_title,
                'show_testimonials': show_testimonials,
                'trial_length':trial_length,
                'tag_break_lines': tag_break_lines,
                'paid_site':paid_site,
                'show_power_electronics':show_power_electronics,
                'show_ana_electronics':show_ana_electronics,
                'show_dig_electronics':show_dig_electronics,
                'input_voltage':input_voltage,
                'output_voltage':output_voltage,
                'output_current':output_current,
                'q1_on_res':q1_on_res,
                'd1_on_volt':d1_on_volt,
                'inductor_res':inductor_res,
                'capacitor_res':capacitor_res,
                'inductance':inductance,
                'capacitance':capacitance,
                'bode_x_range': bode_x_range,
                'mags': mags,
                'phases':phases,
                'mags_min':mags_min,
                'mags_max':mags_max,
                'phase_min':phase_min,
                'phase_max':phase_max}
    )