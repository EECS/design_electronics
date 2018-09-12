from django.http import JsonResponse
from django.shortcuts import render
from itertools import chain

#Import Power Electronics portion of the website for left sidebar
from .models import DCDC
#Import design parameter forms
from .forms import DesignParamForm, DesignCompForm, abbrev_design_params, abbrev_component_params
from .smps_views_helper import generate_rec_dcdc_components, analyze_dcdc_converter, generate_sidebar
from .smps_views_helper import generate_bode
import json

context = {}
design_param_form = 0

# Create your views here.
def smps(request):
    #Design parameters received flag and recommended components updated flags set to false on page load.
    design_param_updated = False
    design_comp_updated = False

    if request.method == "GET":
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

        analyzed_circuit_object = None
        circuit_found = False

        #Loop through all models and select a model object to be displayed on webpage.
        for circuit_type in models:
            filtered_circuit = circuit_type.filter(url=analyzed_circuit_url)
            if len(filtered_circuit) == 1:
                circuit_found = True
                analyzed_circuit_object = filtered_circuit[0]
                break

        #####################################
        #Generate the sidebar.              #
        #####################################
        generate_sidebar(power_types, smps_types, dc_dc_types, dc_dc_list, context)

        #Render 404 page if circuit url was not found.
        if not circuit_found:
            return render(
                request,
                '404.html',
                context=context
            )
    
        context.update({'analyzed_circuit_object': analyzed_circuit_object})

        #####################################
        #Generate the design parameters and #
        #selected components forms.         #
        #####################################
        design_parameters_circuit_object = analyzed_circuit_object.design_params.all()
        selected_components_circuit_object = analyzed_circuit_object.selected_components.all()

        context.update({'design_parameters_circuit_object': design_parameters_circuit_object})
        context.update({'selected_components_circuit_object': selected_components_circuit_object})

        design_param_form = DesignParamForm(None, design_parameters_circuit_object)
        design_comp_form = DesignCompForm(None, selected_components_circuit_object)

        context.update({'design_param_form': design_param_form, 'design_comp_form':design_comp_form })

        #GET method, populate recommended components section with default text.
        generate_rec_dcdc_components(analyzed_circuit_object, context, None)
        analyze_dcdc_converter(analyzed_circuit_object, context, None)

        #Initial flags for receiving updated forms are set to false on initial page load.
        context.update({'design_comp_updated': False})
        context.update({'design_param_updated': False})

        #Populate bode plots with initial load of data.
        generate_bode(analyzed_circuit_object, context, None, 5000)

    #####################################
    #Generate the recommended components#
    #or analyze the circuit.
    #####################################
    elif request.method == "POST":

        #Generate selected components.
        if "submitdesignparams" in request.POST:
            design_param_form = DesignParamForm(request.POST, context["design_parameters_circuit_object"])
            circuit_obj = context["analyzed_circuit_object"]

            #Validate data (and generate self.cleaned_data) 
            #prior to custom clean so that it is available
            #to custom cleaning method.
            design_param_form.is_valid()
            #Custom clean design_param_form given type of power electronic circuit to be analyzed.
            design_param_form.custom_clean(circuit_obj.pe_circuit_type, circuit_obj.smps_circuit_type,
                                    circuit_obj.dcdc_type, circuit_obj.name)

            if len(design_param_form.errors) == 0:
                generate_rec_dcdc_components(context["analyzed_circuit_object"], context, design_param_form.cleaned_data)

                #Update design parameter form
                context.update({'design_param_form': design_param_form})
                context.update({'design_param_updated': True})
            else:
                #The entered data was not valid, return errors.
                context.update({'design_param_updated': False})
                response = JsonResponse({"errors": design_param_form.errors})
                response.status_code = 403

                return response

            return JsonResponse(context["rec_dcdc_comps"], safe=False)

        #Analyze the circuit.
        elif "submitcompvalues" in request.POST:
            #Checks if the first recommended component has been populated
            #given valid design parameters.
            if context["design_param_updated"]:
                design_comp_form = DesignCompForm(request.POST, context["selected_components_circuit_object"])
                circuit_obj = context["analyzed_circuit_object"]

                #Validate data (and generate self.cleaned_data) 
                #prior to custom clean so that it is available
                #to custom cleaning method.
                design_comp_form.is_valid()
                #Custom clean design_param_form given type of power electronic circuit to be analyzed.
                design_comp_form.custom_clean(circuit_obj.pe_circuit_type, circuit_obj.smps_circuit_type,
                                    circuit_obj.dcdc_type, circuit_obj.name)
                
                if design_comp_form.is_valid():
                    design_param_form = context["design_param_form"]
                    success = analyze_dcdc_converter(context["analyzed_circuit_object"], context, dict(chain(design_comp_form.cleaned_data.items(), 
                                                                                        design_param_form.cleaned_data.items())))
                    if success:
                        context.update({'design_comp_form': design_comp_form})
                        context.update({'design_comp_updated': True})
                    else:
                        context.update({'design_comp_updated': False})
                        param_error = {}
                        param_error["DC/DC Analysis"]= ["Design components selected do not result in a feasible converter." + 
                        " Possible issues could be due to the losses in the parasitic resistances, reduce values and resubmit. "]

                        response = JsonResponse({"errors": param_error})
                        response.status_code = 403

                        return response
                else:
                    #The entered data was not valid.
                    context.update({'design_comp_updated': False})
                    response = JsonResponse({"errors": design_comp_form.errors})
                    response.status_code = 403

                    return response

                return JsonResponse(context["analyzed_equations"], safe=False)
            else:
                #Design parameters were not received, must enter design parameters
                #before being able to analyze the converter.
                context.update({'design_comp_updated': False})
                design_comp_form = DesignCompForm(request.POST, context["selected_components_circuit_object"])

                #Get a field to associate an error with. NEED TO UPDATE, THIS IS TERRIBLE.
                for k, v in design_comp_form.fields.items():
                    field = k
                    break

                design_comp_form.add_error(field, "Design parameter form entered was not valid." + 
                " Correct form and resubmit prior to submitting component values.")

                response = JsonResponse({"errors": design_comp_form.errors})
                response.status_code = 403

                return response

        #Generate open loop bode plots
        elif "generateopenplots" in request.POST:

            #Both design parameter form and design component form must be filled out to 
            #generate open loop plots.
            if context["design_param_updated"] and context["design_comp_updated"]:

                design_comp_form = context["design_comp_form"]
                design_param_form = context["design_param_form"]
                cleaned_data = dict(chain(design_comp_form.cleaned_data.items(), design_param_form.cleaned_data.items(), [("D",context["duty_cycle"])]))
                updated_data = generate_bode(context["analyzed_circuit_object"], context, cleaned_data, 5000)

                return JsonResponse(updated_data, safe=False)
            else:
                if not(context["design_param_updated"]):
                    #Design parameters were not received, must enter design parameters
                    #before being able to analyze the converter.

                    param_error = {}
                    param_error["Design parameter form"] = ("Design parameter form entered was not valid." + 
                    " Correct form and resubmit prior to generating open loop bode plots.")
                    
                    response = JsonResponse({"errors": param_error})

                elif not(context["design_comp_updated"]):
                    #Design components were not received, must enter design components
                    #before being able to analyze the converter.

                    param_error = {}
                    param_error["Design component form"]= ["Design component form entered was not valid." + 
                    " Correct form and resubmit prior to generating open loop bode plots."]
                    
                    response = JsonResponse({"errors": param_error})

                response.status_code = 403

                return response

    return render(
        request,
        'smps.html',
        context=context
    )