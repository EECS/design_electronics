from django.shortcuts import render
import math, re, cmath
from .models import ConverterEquation
from .views_helper import js_math, generate_bode

# Create your views here.
def home(request):
    context = {}
    #####################################
    #Other web page parameters
    #####################################
    design_center_url = "/design-center"
    context.update({'design_center_url': design_center_url})

    #####################################
    #Index.html parameters
    #####################################
    show_testimonials = False
    paid_site = False
    trial_length = 14
    header_title = "Design Electronics"
    tag_break_lines = range(6)

    show_power_electronics = True
    show_ana_electronics = False
    show_dig_electronics = True
    
    context.update({'show_testimonials': show_testimonials, 'paid_site': paid_site, 'trial_length': trial_length, 'header_title': header_title,
                    'tag_break_lines': tag_break_lines, 'show_power_electronics': show_power_electronics, 'show_ana_electronics': show_ana_electronics,
                    'show_dig_electronics':show_dig_electronics})

    #####################################
    #Circuit Parameters Context Update  #
    #####################################

    #Circuit Parameters
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

    context.update({'input_voltage': input_voltage, 'output_voltage': output_voltage, 'output_current': output_current, 'q1_on_res': q1_on_res,
                    'd1_on_volt': d1_on_volt, 'inductor_res': inductor_res, 'capacitor_res': capacitor_res, 'inductance': round(inductance*1e6),
                    'capacitance': capacitance})

    #####################################
    #Model Parameters
    #####################################
    #Query database for landing page example and select first instance.
    analyzed_circuit_object = ConverterEquation.objects.filter(name="Landing Page Example")[0]

    ########################################
    #Bode Plot generation
    ########################################

    generate_bode(analyzed_circuit_object, context, num_points=5000)

    return render(
        request,
        'landing_page.html',
        context=context
    )