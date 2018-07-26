from django.http import JsonResponse
from django.shortcuts import render
from itertools import chain

#Import Power Electronics portion of the website for left sidebar
from .models import DCDC
#Import design parameter forms
from .forms import DesignParamForm, DesignCompForm, abbrev_design_params, abbrev_component_params
from .smps_views_helper import generate_rec_dcdc_components, analyze_converter, generate_sidebar
from .smps_views_helper import js_math, generate_bode

context = {}

# Create your views here.
def home(request):
    #####################################
    #Generic website parameters
    #####################################
    landing_page_url = "/"
    design_center_url = "design-center"
    header_title = "Design Electronics"
    context.update({"landing_page_url": landing_page_url, "design_center_url": design_center_url, 'header_title': header_title})

    #####################################
    #Model Parameters
    #####################################
    #Create list of all models in database.
    models = []

    #Query DC DC converters.
    dc_dc_query = DCDC.objects.all()
    models.append(dc_dc_query)

    #Assumes that DC DC converter model has at least one entry.
    if len(dc_dc_query) != 0:
        power_types = dc_dc_query[0].POWER_ELECTRONIC_CIRCUIT_TYPES
        smps_types = dc_dc_query[0].SMPS_TYPES
        dc_dc_types = dc_dc_query[0].DCDC_TYPES
        dc_dc_list = [o for o in dc_dc_query]

    #####################################
    #Current Circuit Analysis Update    #
    #####################################
    default_circuit_url = "ccm-buck-converter"
    analyzed_circuit_url = request.path.rsplit("/", 1)[1]

    #Handle design-center page default design shown.
    if analyzed_circuit_url == design_center_url:
        analyzed_circuit_url = default_circuit_url

    ####HANDLE 404.#########

    analyzed_circuit_object = None
    circuit_found = False

    #Loop through all models and select a model object to be displayed on webpage.
    for circuit_type in models:
        filtered_circuit = circuit_type.filter(url=analyzed_circuit_url)
        if len(filtered_circuit) == 1:
            circuit_found = True
            analyzed_circuit_object = filtered_circuit[0]
            break

    if not circuit_found:
        #Throw 404
        pass
    
    context.update({'analyzed_circuit_object': analyzed_circuit_object})
    #####################################
    #Generate the sidebar.              #
    #####################################
    generate_sidebar(power_types, smps_types, dc_dc_types, dc_dc_list, context)

    #####################################
    #Generate the design parameters and #
    #selected components forms.         #
    #####################################
    design_parameters_circuit_object = analyzed_circuit_object.design_params.all()
    selected_components_circuit_object = analyzed_circuit_object.selected_components.all()

    design_param_form = DesignParamForm(None, design_parameters_circuit_object)
    design_comp_form = DesignCompForm(None, selected_components_circuit_object)

    context.update({'design_param_form': design_param_form, 'design_comp_form':design_comp_form })

    #####################################
    #Generate the recommended components#
    #or analyze the circuit.
    #####################################
    if request.method == "POST":
        #Generate selected components.
        if "submitdesignparams" in request.POST:
            design_param_form = DesignParamForm(request.POST, design_parameters_circuit_object)
            if design_param_form.is_valid():
                generate_rec_dcdc_components(analyzed_circuit_object, context, design_param_form.cleaned_data)
            else:
                #The entered data was not valid
                generate_rec_dcdc_components(analyzed_circuit_object, context, None)

            return JsonResponse(context["rec_dcdc_comps"], safe=False)

        #Analyze the circuit.
        elif "submitcompvalues" in request.POST:
            #Checks if the first recommended component has been populated
            #given valid design parameters. Validation method is to check if
            # units have been populated.
            if context["rec_dcdc_comps"][0][4] != '':
                design_comp_form = DesignParamForm(request.POST, selected_components_circuit_object)
                if design_comp_form.is_valid():
                    #analyze_converter(context)
                    pass
                else:
                    #The entered data was not valid.
                    pass
            else:
                print("Design parameters not received. Please enter design parameters and submit, and then resubmit the selected component values.")
                return JsonResponse("Test", safe=False)
        else:
            print("DIDN'T WORK")
    #GET method, populate recommended components section with default text.
    else:
        generate_rec_dcdc_components(analyzed_circuit_object, context, None)

    #####################################
    #Generate bode plot data.           #
    #####################################
    input_output_transfer = analyzed_circuit_object.input_output_transfer
    input_impedance = analyzed_circuit_object.input_impedance
    output_impedance = analyzed_circuit_object.output_impedance
    duty_output_transfer = analyzed_circuit_object.duty_output_transfer

    #generate_bode(input_output_transfer, input_impedance, output_impedance, duty_output_transfer, context)

    return render(
        request,
        'home.html',
        context=context
    )