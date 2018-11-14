from django.db import models
from .model_pkg import DesignParamChoices, SelectedComponents, RecommendedComponents, OpenLoopAnalysisEquations

class PowerElectronics(models.Model):
    """
    Model representing Power Electronic circuits
    """
    POWER_ELECTRONIC_CIRCUIT_TYPES = [
        ("SMPS", "Switch-Mode Power Supplies")
    ]

class SMPS(models.Model):
    """
    Model representing Switch Mode Power Supply Circuits
    """

    SMPS_TYPES = [
        ("DCDC", "DC-DC Converters")
    ]

class DCDC(models.Model):
    """
    Model representing Power Electronic circuits
    """
    POWER_ELECTRONIC_CIRCUIT_TYPES = PowerElectronics.POWER_ELECTRONIC_CIRCUIT_TYPES

    SMPS_TYPES = SMPS.SMPS_TYPES

    DCDC_TYPES = [
        ("CCM", "Continuous Conduction Mode")
    ]

    pe_circuit_type = models.CharField(max_length=1000, help_text="Enter the type of power electronic circuit to be modeled.", choices=POWER_ELECTRONIC_CIRCUIT_TYPES)

    smps_circuit_type = models.CharField(max_length=1000, help_text="Enter the type of switch mode power supply to be modeled.", choices=SMPS_TYPES)

    dcdc_type = models.CharField(max_length=1000, help_text="Enter the type of DC-DC converter to be modeled.", choices=DCDC_TYPES)

    name = models.CharField(max_length=1000, help_text="Enter the name of this converter in the admin page. REQUIRED.")
    url = models.CharField(max_length=1000, help_text="Enter the url to be used to access this model. REQUIRED.", default=str(1))

    description = models.TextField(help_text="Enter a description of the circuit to be modeled.", default=str(1))

    design_params = models.ManyToManyField(DesignParamChoices)

    recommended_components = models.ManyToManyField(RecommendedComponents)

    selected_components = models.ManyToManyField(SelectedComponents)

    open_loop_analysis_equations = models.ManyToManyField(OpenLoopAnalysisEquations, help_text="For example, efficient, output current, etc.")

    #Open loop bode plots of the converter.
    open_input_output_transfer = models.TextField(max_length=5000, help_text="Enter the input to output transfer function of the converter.",
                                                    default="Default.")
    open_input_impedance = models.TextField(max_length=5000, help_text="Enter the input impedance of the converter.",
                                                    default="Default.")
    open_output_impedance = models.TextField(max_length=5000, help_text="Enter the output impedance of the converter.",
                                                    default="Default.")
    open_duty_output_transfer = models.TextField(max_length=5000, help_text="Enter the duty to output transfer function of the converter.",
                                                    default="Default.")

    closed_loop_analysis = models.BooleanField(help_text="Check if this DC/DC converter will be analyzed in a closed-loop fashion.", default=False)

    #Closed loop bode plots of the converter.
    closed_input_output_transfer = models.TextField(max_length=5000, help_text="Enter the input to output transfer function of the converter.",
                                                    default="Default.")
    closed_input_impedance = models.TextField(max_length=5000, help_text="Enter the input impedance of the converter.",
                                                    default="Default.")
    closed_output_impedance = models.TextField(max_length=5000, help_text="Enter the output impedance of the converter.",
                                                    default="Default.")
    closed_duty_output_transfer = models.TextField(max_length=5000, help_text="Enter the duty to output transfer function of the converter.",
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
        verbose_name = "DC/DC Model"
        verbose_name_plural = "DC/DC Models"