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
        verbose_name_plural = "Design Parameters"

class DCDCSelectedComponents(models.Model):
    selected_components_for_analysis = models.CharField(max_length = 100)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.selected_components_for_analysis
        
    def __unicode__(self):
        return self.selected_components_for_analysis

    class Meta:
        ordering = ['selected_components_for_analysis']
        verbose_name = "Selected Component"
        verbose_name_plural = "DC/DC Selected Components"

class DCDCRecommendedComponents(models.Model):
    components = models.CharField(max_length = 100)
    circuit_name = models.CharField(max_length=200, help_text="Enter the name of this converter in the admin page.", default=str(1))
    equation = models.TextField(max_length=5000, help_text="Enter the equation used to generate this recommended component.", default=str(1))

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.components + ", " + self.circuit_name
        
    def __unicode__(self):
        return self.components

    class Meta:
        ordering = ['components']
        verbose_name = "component"
        verbose_name_plural = "DC/DC Recommended Components"

class DCDCOpenLoopAnalysisEquations(models.Model):
    circuit_url = models.CharField(max_length = 200)
    equation_name = models.CharField(max_length = 200)
    equation = models.TextField(max_length=1000, help_text="Enter the equation to be used to analyze the converter.", default=str(1))
    units = models.CharField(max_length = 200, help_text="Enter the units of the resulting equation.", default=str(1))

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.circuit_url + ", " + self.equation_name
        
    def __unicode__(self):
        return self.circuit_url

    class Meta:
        ordering = ['circuit_url']
        verbose_name = "DC/DC Analysis Equation"
        verbose_name_plural = "DC/DC Open-Loop Analysis Equations"

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

    selected_components = models.ManyToManyField(DCDCSelectedComponents)

    open_loop_analysis_equations = models.ManyToManyField(DCDCOpenLoopAnalysisEquations)

    #Open loop bode plots of the converter.
    input_output_transfer = models.TextField(max_length=5000, help_text="Enter the input to output transfer function of the converter.")
    input_impedance = models.TextField(max_length=5000, help_text="Enter the input impedance of the converter.")
    output_impedance = models.TextField(max_length=5000, help_text="Enter the output impedance of the converter.")
    duty_output_transfer = models.TextField(max_length=5000, help_text="Enter the duty to output transfer function of the converter.")

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