from django.db import models

#Import all models from power_models.py 
from .power_models import DCDC, DesignParamChoices, RecommendedComponents, SelectedComponents, OpenLoopAnalysisEquations

#Import all models from fpga_models.py 
from .fpga_models import FPGA

#Import all models from fpga_models.py 
from .analog_models import Analog

class CircuitDesign(models.Model):
    CIRCUIT_TYPES = [
        ("FPGA", "FPGA Design"),
        ("Analog", "Analog Circuit Design"),
        ("Power", "Power Electronics Circuit Design"),
    ]

    circuit_name = models.CharField(help_text="Enter a circuit name for information only at the top level. Circuit names will be contained in individual model fields.",
                                    max_length=1000, default="Test")
    circuit_design_type = models.CharField(max_length=1000, default=CIRCUIT_TYPES[0], help_text="Enter the type of circuit of this circuit to be analyzed.", choices=CIRCUIT_TYPES)

    dc_dc_circuit_analysis = models.BooleanField(help_text="Check if this is DC/DC Circuit Analysis", default=False)
    dc_dc_analysis = models.ManyToManyField(DCDC)

    fpga_analysis = models.BooleanField(help_text="Check if this is FPGA Circuit Analysis", default=False)
    fpga_design = models.ManyToManyField(FPGA)
    analog_analysis = models.BooleanField(help_text="Check if this is Analog Circuit Analysis", default=False)
    analog_design = models.ManyToManyField(Analog)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.circuit_name