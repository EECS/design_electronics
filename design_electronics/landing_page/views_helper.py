import math, re, cmath

def js_math(initial_load, transfer_function, context, num_points = 5000):
    #Circuit Parameters
    input_voltage = context["input_voltage"]
    output_voltage = context["output_voltage"]
    output_current = context["output_current"]
    q1_on_res = context["q1_on_res"]
    d1_on_volt = context["d1_on_volt"]
    inductor_res = context["inductor_res"]
    capacitor_res = context["capacitor_res"]
    inductance = context["inductance"]
    capacitance = context["capacitance"]

    start_frequency = 1 #Hz
    end_frequency = 1000 #kHz
    log_step_size = ((math.log10(end_frequency*1000)-math.log10(start_frequency))/num_points)

    bode_x_range = [10**((i+1)*log_step_size) for i in range(num_points)]
    phases = []
    mags = []

    #Initial load of page, need to set bode plot to 0 dB and 0 degrees.
    if initial_load:
        mags = [0 for point in bode_x_range]
        phases = [0 for point in bode_x_range]
    else:
        #Define circuit parameters to graph
        vals = {"Vin": str(input_voltage), "VD1":str(d1_on_volt), "RQ1":str(q1_on_res/1000), "Vo": str(output_voltage), "Io":str(output_current),
                'L1': str(inductance/1000000), 'RL1':str(inductor_res/1000), "RC1":str(capacitor_res/1000), "C1": str(capacitance/1000000), "D": str(output_voltage/input_voltage)}
        #Replace symbols with values defined in vals dictionary
        for k, v in vals.items():
            #Find key and only the key. Example, finds R1 and not R11 by separating on the non-word boundary.
            transfer_function = re.sub(r"\b"+k+r"\b", v, transfer_function)

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

def generate_bode(initial_load, analyzed_circuit_object, context, num_points = 5000):
    """
    Creates bode plots and updates the context statement to be used to create webpage
    input_output_transfer - Input to output transfer function
    input_impedance - Input impedance transfer function
    output_impedance - Output impedance transfer function
    duty_output_transfer - Duty to output transfer function
    """

    input_output_transfer = analyzed_circuit_object.input_output_transfer
    input_impedance = analyzed_circuit_object.input_impedance
    output_impedance = analyzed_circuit_object.output_impedance
    duty_output_transfer = analyzed_circuit_object.duty_output_transfer

    updated_data = []

    ########################################
    #Bode Plot parameters - Output Impedance
    ########################################
    out_imped_mag_div = "out-imped-mag-div"
    out_imped_phs_div = "out-imped-phs-div"
    bode_x_range_output_impedance, mags_output_impedance, phases_output_impedance = js_math(initial_load, output_impedance, context, num_points)
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

    updated_data.append([out_imped_mag_div, mags_output_impedance, mags_min_output_impedance, 
                        mags_max_output_impedance, phases_output_impedance, phase_min_output_impedance, 
                        phase_max_output_impedance])
    ########################################
    #Bode Plot parameters - Input Impedance
    ########################################
    in_imped_mag_div = "in-imped-mag-div"
    in_imped_phs_div = "in-imped-phs-div"
    bode_x_range_input_impedance, mags_input_impedance, phases_input_impedance = js_math(initial_load, input_impedance, context, num_points)
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

    updated_data.append([in_imped_mag_div, mags_input_impedance, mags_min_input_impedance, 
                        mags_max_input_impedance, phases_input_impedance, phase_min_input_impedance, 
                        phase_max_input_impedance])
    ################################################
    #Bode Plot parameters - Input to Output Transfer
    ################################################
    in_out_mag_div = "in-out-mag-div"
    in_out_phs_div = "in-out-phs-div"
    bode_x_range_input_output_transfer, mags_input_output_transfer, phases_input_output_transfer = js_math(initial_load, input_output_transfer, context, num_points)
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

    updated_data.append([in_out_mag_div, mags_input_output_transfer, mags_min_input_output_transfer, 
                        mags_max_input_output_transfer, phases_input_output_transfer, phase_min_input_output_transfer, 
                        phase_max_input_output_transfer])
    ################################################
    #Bode Plot parameters - Duty to Output Transfer
    ################################################
    duty_out_mag_div = "duty-out-mag-div"
    duty_out_phs_div = "duty-out-phs-div"
    bode_x_range_duty_output_transfer, mags_duty_output_transfer, phases_duty_output_transfer = js_math(initial_load, duty_output_transfer, context, num_points)
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

    updated_data.append([duty_out_mag_div, mags_duty_output_transfer, mags_min_duty_output_transfer, 
                        mags_max_duty_output_transfer, phases_duty_output_transfer, phase_min_duty_output_transfer, 
                        phase_max_duty_output_transfer])
    
    return updated_data