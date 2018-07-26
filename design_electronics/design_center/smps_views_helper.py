import math, re, cmath
#Import design parameter forms
from .forms import abbrev_design_params, abbrev_component_params
from itertools import chain

def analyze_dcdc_converter(analyzed_circuit_object, context, cleaned_data=None):
    '''
    Analyzes the converter for design for DC/DC converters.
    Inputs: model circuit object, context list,
    cleaned_data dictionary generated from form  

    Outputs: Void, updates the context dictionary with the recommended component
    values in the rec_dcdc_comps variable. Example of updated rec_dcdc_comps:
    [["Output Capacitor", "C1", "100" (uF), "F"], ["Output Inductor", "L1", "10" (uH), "H"]]
    '''
    analyzed_equations = []
    
    #Retrieve all components for which recommended design selection will occur.
    dcdc_analysis_eqs = analyzed_circuit_object.recommended_components.all()

    for comp in dcdc_comp_equations:
        parsed_name = comp.components.split(",")
        #Component design equation.
        eq_symbols = comp.equation
        eq = eq_symbols

        #Initial load of the page.
        if cleaned_data == None:
            rec_dcdc_comps.append([parsed_name[1], parsed_name[0], eq_symbols, "Enter design parameters to generate recommended component values.", ""])
        else:

            #Loop through all keys (abbreviations) and replace with cleaned value.
            for k, v in abbrev_design_params.items():
                #Find key and only the key. Example, finds R1 and not R11 by separating on the non-word boundary.
                eq = re.sub(r"\b"+k+r"\b", str(cleaned_data[abbrev_design_params[k]]), eq)

            denom_start = eq.find("/")

            #Create numerator and denominator strings of the transfer function.
            if denom_start != -1:
                numerator = eq[:denom_start]
                denominator = eq[denom_start+1:]
            else:
                numerator = eq
                denominator = str(1)

            num = eval(numerator)
            denom = eval(denominator)

            if denom == 0:
                rec_dcdc_comps.append([parsed_name[1], parsed_name[0], "Invalid input parameters, equation caused an infinite value.", ""])
            else:

                if "c" in parsed_name[0].lower():
                    units = "F"
                else:
                    units = "H"

                rec_dcdc_comps.append([parsed_name[1], parsed_name[0], eq_symbols, str(round((num/denom)*1e6, 2)), units])

    context.update({"rec_dcdc_comps": rec_dcdc_comps})

def generate_rec_dcdc_components(analyzed_circuit_object, context, cleaned_data=None):
    '''
    Generates recommended component values for design for DC/DC converters.
    Inputs: cleaned_data dictionary generated from 

    Outputs: Void, updates the context dictionary with the recommended component
    values in the rec_dcdc_comps variable. Example of updated rec_dcdc_comps:
    [["Output Capacitor", "C1", "100" (uF), "F"], ["Output Inductor", "L1", "10" (uH), "H"]]
    '''
    rec_dcdc_comps = []
    
    #Retrieve all components for which recommended design selection will occur.
    dcdc_comp_equations = analyzed_circuit_object.recommended_components.all()

    for comp in dcdc_comp_equations:
        parsed_name = comp.components.split(",")
        #Component design equation.
        eq_symbols = comp.equation
        eq = eq_symbols

        #Initial load of the page.
        if cleaned_data == None:
            rec_dcdc_comps.append([parsed_name[1], parsed_name[0], eq_symbols, "Enter design parameters to generate recommended component values.", ""])
        else:

            #Loop through all keys (abbreviations) and replace with cleaned value.
            for k, v in abbrev_design_params.items():
                #Find key and only the key. Example, finds R1 and not R11 by separating on the non-word boundary.
                eq = re.sub(r"\b"+k+r"\b", str(cleaned_data[abbrev_design_params[k]]), eq)

            denom_start = eq.find("/")

            #Create numerator and denominator strings of the transfer function.
            if denom_start != -1:
                numerator = eq[:denom_start]
                denominator = eq[denom_start+1:]
            else:
                numerator = eq
                denominator = str(1)

            num = eval(numerator)
            denom = eval(denominator)

            if denom == 0:
                rec_dcdc_comps.append([parsed_name[1], parsed_name[0], "Invalid input parameters, equation caused an infinite value.", ""])
            else:

                if "c" in parsed_name[0].lower():
                    units = "F"
                else:
                    units = "H"

                rec_dcdc_comps.append([parsed_name[1], parsed_name[0], eq_symbols, str(round((num/denom)*1e6, 2)), units])

    context.update({"rec_dcdc_comps": rec_dcdc_comps})

def generate_sidebar(pe_list, smps_list, dc_dc_types, dc_dc_list, context):
    """ Generates the sidebar for the webpage. Passed the following variables:
    Returns a sidebar_list 4th dimensional list variable with the following indices:
    sidebar_list[pe_circuit_type]...
    e.g.sidebar_list[smps][dc-dc][ccm/dcm][[buck-converter]]
    """
    sidebar_list = []
    sidebar_list.append([pe[1]for pe in pe_list])
    sidebar_list.append([[smps[1] for smps in smps_list]])
    sidebar_list.append([[[dctypes[1] for dctypes in dc_dc_types]]])

    ccm_converters = []
    dcm_converters = []

    for dc in dc_dc_list:
        converter_index = 3
        ccm_index = 0
        dcm_index = 1
        if dc.dcdc_type == "CCM":
            #List does not contain any converters yet, handle 0 edge case.
            #Add first CCM converter as well as blank list for first DCM converter
            #to handle 0 edge case.
            if len(sidebar_list) == converter_index:
                sidebar_list.append([[[[dc],[]]]])
            else:
                sidebar_list[converter_index][ccm_index].append(dc)
        elif dc.dcdc_type == "DCM":
            #List does not contain any converters yet, handle 0 edge case.
            #Add first DCM converter as well as blank list for first CCM converter
            #to handle 0 edge case.
            if len(sidebar_list) == converter_index:
                sidebar_list.append([[[[],[dc]]]])
            else:
                sidebar_list[converter_index][dcm_index].append(dc)
    
    context.update({"sidebar_list": sidebar_list})

    #print("TEST "+ str(sidebar_list))

def js_math(transfer_function):
    num_points = 5000

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

def generate_bode(input_output_transfer, input_impedance, output_impedance, duty_output_transfer, context):
    """
    Creates bode plots and updates the context statement to be used to create webpage
    input_output_transfer - Input to output transfer function
    input_impedance - Input impedance transfer function
    output_impedance - Output impedance transfer function
    duty_output_transfer - Duty to output transfer function
    """
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