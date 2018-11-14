from django.db import models
from .model_pkg import DesignParamChoices, SelectedComponents, RecommendedComponents, OpenLoopAnalysisEquations

class FPGA(models.Model):
    """
    Model representing Power Electronic circuits
    """
    FPGA_CIRCUIT_TYPES = [
        ("Controllers", "Controller")
    ]

    fpga_circuit_type = models.CharField(max_length=1000, help_text="Enter the type of power electronic circuit to be modeled.", choices=FPGA_CIRCUIT_TYPES)

    name = models.CharField(max_length=1000, help_text="Enter the name of this converter in the admin page. REQUIRED.")
    url = models.CharField(max_length=1000, help_text="Enter the url to be used to access this model. REQUIRED.", default=str(1))

    description = models.TextField(help_text="Enter a description of the circuit to be modeled.", default=str(1))

    fpga_code = models.TextField(help_text="Please enter the VHDL code for the FPGA design.", default="Default.")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.fpga_circuit_type+ " " + self.name
        
    def get_absolute_url(self):
        """
        Returns the url to access.
        """
        pass
    
    class Meta:
        ordering = ['name']
        verbose_name = "FPGA Model"
        verbose_name_plural = "FPGA Models"