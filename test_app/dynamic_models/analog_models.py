from django.db import models
from .model_pkg import DesignParamChoices, SelectedComponents, RecommendedComponents, OpenLoopAnalysisEquations

class AnalogElectronics(models.Model):
    """
    Model representing Power Electronic circuits
    """
    ANALOG_ELECTRONICS_CIRCUIT_TYPES = [
        ("Active Filters", "Active Filter"),
        ("Passive Filters", "Passive Filter")
    ]

class Analog(models.Model):
    """
    Model representing Power Electronic circuits
    """
    ANALOG_TYPES = AnalogElectronics.ANALOG_ELECTRONICS_CIRCUIT_TYPES

    analog_type = models.CharField(max_length=1000, help_text="Enter the type of analog circuit to be modeled.", choices=ANALOG_TYPES)

    name = models.CharField(max_length=1000, help_text="Enter the name of this design in the admin page. REQUIRED.")
    url = models.CharField(max_length=1000, help_text="Enter the url to be used to access this model. REQUIRED.", default=str(1))

    description = models.TextField(help_text="Enter a description of the circuit to be modeled.", default=str(1))

    design_params = models.ManyToManyField(DesignParamChoices)

    recommended_components = models.ManyToManyField(RecommendedComponents)

    selected_components = models.ManyToManyField(SelectedComponents)

    open_loop_analysis_equations = models.ManyToManyField(OpenLoopAnalysisEquations, help_text="For example, efficient, output current, etc.")

    #Open loop bode plots of the analog design.
    open_input_output_transfer = models.TextField(max_length=5000, help_text="Enter the input to output transfer function of the design.",
                                                    default="Default.")
    open_input_impedance = models.TextField(max_length=5000, help_text="Enter the input impedance of the design.",
                                                    default="Default.")
    open_output_impedance = models.TextField(max_length=5000, help_text="Enter the output impedance of the design.",
                                                    default="Default.")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.dcdc_type+ " " + self.name
        
    def get_absolute_url(self):
        """
        Returns the url to access.
        """
        pass
    
    class Meta:
        ordering = ['name']
        verbose_name = "Analog Model"
        verbose_name_plural = "Analog Models"