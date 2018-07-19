from django.db import models

class PowerElectronics(models.Model):
    """
    Model representing Power Electronic circuits
    """
    POWER_ELECTRONIC_CIRCUIT_TYPES = [
        ("SMPS", "Switch-Mode Power Supplies")
    ]

    name = models.CharField(max_length=200, help_text="Enter the name of the type of power electronic circuit to be analyzed.", choices=POWER_ELECTRONIC_CIRCUIT_TYPES)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
    def get_absolute_url(self):
        """
        Returns the url to access.
        """
        pass

class SMPS(models.Model):
    """
    Model representing Switch Mode Power Supply Circuits
    """

    SMPS_TYPES = [
        ("DCDC", "DC-DC Converters")
    ]

    name = models.CharField(max_length=200, help_text="Enter the name of the type of SMPS circuit to be stored.", choices=SMPS_TYPES)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
    def get_absolute_url(self):
        """
        Returns the url to access.
        """
        pass

class DesignParamChoices(models.Model):
    params = models.CharField(max_length = 100)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.params
        
    def __unicode__(self):
        return self.params

    class Meta:
        ordering = ['params']
        verbose_name = "param"
        verbose_name_plural = "params"

class DCDCRecommendedComponents(models.Model):
    components = models.CharField(max_length = 100)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.components
        
    def __unicode__(self):
        return self.components

    class Meta:
        ordering = ['components']
        verbose_name = "component"
        verbose_name_plural = "Components"

class DCDC(models.Model):
    """
    Model representing Power Electronic circuits
    """
    POWER_ELECTRONIC_CIRCUIT_TYPES = PowerElectronics.POWER_ELECTRONIC_CIRCUIT_TYPES

    SMPS_TYPES = SMPS.SMPS_TYPES

    DCDC_TYPES = [
        ("CCM", "Continuous Conduction Mode")
    ]

    pe_circuit_type = models.ForeignKey(PowerElectronics, on_delete=models.CASCADE, default=str(1))

    smps_circuit_type = models.ForeignKey(SMPS, on_delete=models.CASCADE)

    dcdc_type = models.CharField(max_length=200, help_text="Enter the type of DC-DC converter to be modeled.", choices=DCDC_TYPES)

    name = models.CharField(max_length=200, help_text="Enter the name of this converter in the admin page.")
    url = models.CharField(max_length=200, help_text="Enter the url to be used to access this model.", default=str(1))

    description = models.TextField(help_text="Enter a description of the circuit to be modeled.", default=str(1))

    design_params = models.ManyToManyField(DesignParamChoices)

    recommended_components = models.ManyToManyField(DCDCRecommendedComponents)

    input_output_transfer = models.TextField(max_length=5000, help_text="Enter the input to output transfer function of the converter.")
    input_impedance = models.TextField(max_length=5000, help_text="Enter the input impedance of the converter.")
    output_impedance = models.TextField(max_length=5000, help_text="Enter the output impedance of the converter.")
    duty_output_transfer = models.TextField(max_length=5000, help_text="Enter the duty to output transfer function of the converter.")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
    def get_absolute_url(self):
        """
        Returns the url to access.
        """
        pass