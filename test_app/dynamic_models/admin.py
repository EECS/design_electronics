from django.contrib import admin

#Import all models from analog_models.py 
from .analog_models import Analog

#Import all models from fpga_models.py 
from .fpga_models import FPGA

#Import all models from power_models.py 
from .power_models import DCDC

#Import all models from model_pkg.py
from .model_pkg import DesignParamChoices, RecommendedComponents, SelectedComponents, OpenLoopAnalysisEquations

#Import all models from models.py
from .models import CircuitDesign

#Register model_pkg.py here.
admin.site.register(DesignParamChoices)
admin.site.register(SelectedComponents)
admin.site.register(RecommendedComponents)
admin.site.register(OpenLoopAnalysisEquations)


class AnalogAdmin(admin.ModelAdmin):
    fieldsets =(
        (None, 
            {
            "fields":('analog_type', 'name', 'url', 'description', 
                    'design_params', 'recommended_components',
                    'selected_components', 'open_loop_analysis_equations',
                    'open_input_output_transfer', 'open_input_impedance',
                    'open_output_impedance')
            }
        ),
    )

class FPGAAdmin(admin.ModelAdmin):
    fieldsets =(
        (None, 
            {
            "fields":('fpga_circuit_type', 'name', 'url', 'description', 
                    'fpga_code')
            }
        ),
    )

class DCDCAdmin(admin.ModelAdmin):
    fieldsets =(
        (None, 
            {
            "fields":('pe_circuit_type', 'smps_circuit_type', 'dcdc_type',
                    'name', 'url', 'description', 'design_params', 'recommended_components',
                    'selected_components', 'open_loop_analysis_equations', 'open_input_output_transfer',
                    'open_input_impedance', 'open_output_impedance', 'open_duty_output_transfer', 
                    'closed_loop_analysis')
            }
        ),
        ("DC/DC Closed Loop Parameters", 
            {
            'classes': ('collapse',),
            "fields":('closed_input_output_transfer', 'closed_input_impedance', 
                    'closed_output_impedance', 'closed_duty_output_transfer')
            }
        ),
    )

class CircuitDesignAdmin(admin.ModelAdmin):
    fieldsets =(
        (None, 
            {
            "fields":('circuit_name', 'circuit_design_type', 'dc_dc_circuit_analysis',),
            }
        ),
        ("DC/DC Converter Parameters", 
            {
            'classes': ('collapse',),
            "fields":('dc_dc_analysis',),
            }
        ),
        (None, 
            {
            "fields":('fpga_analysis',),
            }
        ),
        ("FPGA Design Parameters", 
            {
            'classes': ('collapse',),
            "fields":('fpga_design',),
            }
        ),
        (None, 
            {
            "fields":('analog_analysis',),
            }
        ),
        ("Analog Design Parameters", 
            {
            'classes': ('collapse',),
            "fields":('analog_design',),
            }
        ),
    )

#Register analog_models.py here.
admin.site.register(Analog, AnalogAdmin)

#Register fpga_models.py here.
admin.site.register(FPGA, FPGAAdmin)

#Register power_models.py here.
admin.site.register(DCDC, DCDCAdmin)

# Register models.py here.
admin.site.register(CircuitDesign, CircuitDesignAdmin)