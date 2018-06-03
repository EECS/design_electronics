from django.shortcuts import render
import math, re, cmath
from .models import ConverterEquation

#####################################
#Circuit Parameters
#####################################
fs = 100000
input_voltage = 24
output_voltage = 12
output_current = 1
q1_on_res = 5 #milliOhms
d1_on_volt = 0.7
inductor_res = 5 #milliohms
capacitor_res = 10 #milliohms
inductance = ((input_voltage-output_voltage)/(0.2*output_current))*(output_voltage/input_voltage)*(1/fs)
capacitance = 100 #microfarads
load_res = output_voltage/output_current #ohms

def js_math(transfer_function):
    num_points = 2000

    #print("Transfer function is: " + str(transfer_function) + "\n")

    start_frequency = 1 #Hz
    end_frequency = 50 #kHz
    step_size = int(((end_frequency*1000)-start_frequency)/num_points)

    bode_x_range = [step for step in range(start_frequency, end_frequency*1000, step_size)]

    #Define circuit parameters to graph
    vals = {"Vin": str(input_voltage), "Von":str(d1_on_volt), 'IL':str(output_voltage/load_res), "RQ":str(q1_on_res/1000),
            'L': str(inductance), 'RL':str(inductor_res/1000), "Rc":str(capacitor_res/1000), "C": str(capacitance/1000000), 'Rload': str(load_res), "D": str(output_voltage/input_voltage)}
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
    #print("Transfer function is: " + str(transfer_function) + "\n")

    phases = []
    mags = []

    #Create magnitude and phase arrays for transfer function, replacing s with 
    #the angular frequency representation.
    for f in bode_x_range:
        complex_replace = str(2j*cmath.pi*f)
        complex_replace = "("+complex_replace+")"

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

    #Find and print -3dB point if in list of analyzed frequencies
    #print(next((bode_x_range[mags.index(i)] for i in mags if i <= -3), 'Increase Frequency Range to see -3 dB point of Transfer Function'))
    #Find and print cross over frequency if in list of analyzed frequencies
    #print(next((bode_x_range[phases.index(i)] for i in phases if i <= 0), 'Increase frequency range to see cross over frequency of transfer function'))

    return bode_x_range, mags, phases

# Create your views here.
def index(request):
    context = {}
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
    ###### Context Update ##########
    context.update({'show_testimonials': show_testimonials, 'paid_site': paid_site, 'trial_length': trial_length, 'header_title': header_title,
                    'tag_break_lines': tag_break_lines, 'show_power_electronics': show_power_electronics, 'show_ana_electronics': show_ana_electronics,
                    'show_dig_electronics':show_dig_electronics})

    #####################################
    #Circuit Parameters Context Update  #
    #####################################
    context.update({'input_voltage': input_voltage, 'output_voltage': output_voltage, 'output_current': output_current, 'q1_on_res': q1_on_res,
                    'd1_on_volt': d1_on_volt, 'inductor_res': inductor_res, 'capacitor_res': capacitor_res, 'inductance': round(inductance*1e6),
                    'capacitance': capacitance})

    #####################################
    #Model Parameters
    #####################################
    modelQuery = ConverterEquation.objects.filter(name="Landing Page Example")

    if len(modelQuery) > 0:
        input_output_transfer = modelQuery[0].input_output_transfer
        input_impedance = modelQuery[0].input_impedance
        output_impedance = modelQuery[0].output_impedance
        duty_output_transfer = modelQuery[0].duty_output_transfer

    ########################################
    #Bode Plot parameters - Output Impedance
    ########################################
    out_imped_mag_div = "out-imped-mag-div"
    out_imped_phs_div = "out-imped-phs-div"
    bode_x_range_output_impedance, mags_output_impedance, phases_output_impedance = js_math(output_impedance)
    phase_min_output_impedance = min(phases_output_impedance)
    phase_min_output_impedance -= round(0.5*phase_min_output_impedance)

    phase_max_output_impedance = max(phases_output_impedance)
    phase_max_output_impedance += round(0.5*phase_max_output_impedance)

    mags_min_output_impedance = min(mags_output_impedance)
    mags_min_output_impedance -= round(0.1*mags_min_output_impedance)

    mags_max_output_impedance = max(mags_output_impedance)
    mags_max_output_impedance += round(0.1*mags_max_output_impedance)
    ###### Context Update ##########
    context.update({'bode_x_range_output_impedance': bode_x_range_output_impedance,'mags_output_impedance': mags_output_impedance,
                    'phases_output_impedance': phases_output_impedance, "phase_min_output_impedance": phase_min_output_impedance,
                    'phase_max_output_impedance': phase_max_output_impedance, 'mags_min_output_impedance': mags_min_output_impedance,
                    'mags_max_output_impedance': mags_max_output_impedance, 'out_imped_mag_div': out_imped_mag_div, 'out_imped_phs_div': out_imped_phs_div})

    ########################################
    #Bode Plot parameters - Input Impedance
    ########################################
    in_imped_mag_div = "in-imped-mag-div"
    in_imped_phs_div = "in-imped-phs-div"
    bode_x_range_input_impedance, mags_input_impedance, phases_input_impedance = js_math(input_impedance)
    phase_min_input_impedance = min(phases_input_impedance)
    phase_min_input_impedance -= round(0.5*phase_min_input_impedance)

    phase_max_input_impedance = max(phases_input_impedance)
    phase_max_input_impedance += round(0.5*phase_max_input_impedance)

    mags_min_input_impedance = min(mags_input_impedance)
    mags_min_input_impedance -= round(0.1*mags_min_input_impedance)

    mags_max_input_impedance = max(mags_input_impedance)
    mags_max_input_impedance += round(0.1*mags_max_input_impedance)
    ###### Context Update ##########
    context.update({'mags_input_impedance': mags_input_impedance,
                    'phases_input_impedance': phases_input_impedance, "phase_min_input_impedance": phase_min_input_impedance,
                    'phase_max_input_impedance': phase_max_input_impedance, 'mags_min_input_impedance': mags_min_input_impedance,
                    'mags_max_input_impedance': mags_max_input_impedance, 'in_imped_mag_div': in_imped_mag_div, 'in_imped_phs_div': in_imped_phs_div})

    ################################################
    #Bode Plot parameters - Input to Output Transfer
    ################################################
    in_out_mag_div = "in-out-mag-div"
    in_out_phs_div = "in-out-phs-div"
    bode_x_range_input_output_transfer, mags_input_output_transfer, phases_input_output_transfer = js_math(input_output_transfer)
    phase_min_input_output_transfer = min(phases_input_output_transfer)
    phase_min_input_output_transfer -= round(0.5*phase_min_input_output_transfer)

    phase_max_input_output_transfer = max(phases_input_output_transfer)
    phase_max_input_output_transfer += round(0.5*phase_max_input_output_transfer)

    mags_min_input_output_transfer = min(mags_input_output_transfer)
    mags_min_input_output_transfer -= round(0.1*mags_min_input_output_transfer)

    mags_max_input_output_transfer = max(mags_input_output_transfer)
    mags_max_input_output_transfer += round(0.1*mags_max_input_output_transfer)
    ###### Context Update ##########
    context.update({'mags_input_output_transfer': mags_input_output_transfer,
                    'phases_input_output_transfer': phases_input_output_transfer, "phase_min_input_output_transfer": phase_min_input_output_transfer,
                    'phase_max_input_output_transfer': phase_max_input_output_transfer, 'mags_min_input_output_transfer': mags_min_input_output_transfer,
                    'mags_max_input_output_transfer': mags_max_input_output_transfer, 'in_out_mag_div': in_out_mag_div, 'in_out_phs_div': in_out_phs_div})

    ################################################
    #Bode Plot parameters - Duty to Output Transfer
    ################################################
    duty_out_mag_div = "duty-out-mag-div"
    duty_out_phs_div = "duty-out-phs-div"
    bode_x_range_duty_output_transfer, mags_duty_output_transfer, phases_duty_output_transfer = js_math(duty_output_transfer)
    phase_min_duty_output_transfer = min(phases_duty_output_transfer)
    phase_min_duty_output_transfer -= round(0.5*phase_min_duty_output_transfer)

    phase_max_duty_output_transfer = max(phases_duty_output_transfer)
    phase_max_duty_output_transfer += round(0.5*phase_max_duty_output_transfer)

    mags_min_duty_output_transfer = min(mags_duty_output_transfer)
    mags_min_duty_output_transfer -= round(0.1*mags_min_duty_output_transfer)

    mags_max_duty_output_transfer = max(mags_duty_output_transfer)
    mags_max_duty_output_transfer += round(0.1*mags_max_duty_output_transfer)
    ###### Context Update ##########
    context.update({'mags_duty_output_transfer': mags_duty_output_transfer,
                    'phases_duty_output_transfer': phases_duty_output_transfer, "phase_min_duty_output_transfer": phase_min_duty_output_transfer,
                    'phase_max_duty_output_transfer': phase_max_duty_output_transfer, 'mags_min_duty_output_transfer': mags_min_duty_output_transfer,
                    'mags_max_duty_output_transfer': mags_max_duty_output_transfer, 'duty_out_mag_div': duty_out_mag_div, 'duty_out_phs_div': duty_out_phs_div})

    return render(
        request,
        'index.html',
        context=context
    )