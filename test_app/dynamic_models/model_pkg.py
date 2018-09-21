from django.db import models

class DesignParamChoices(models.Model):
    params = models.CharField(max_length = 1000)

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

class SelectedComponents(models.Model):
    selected_components_for_analysis = models.CharField(max_length = 1000)

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
        verbose_name_plural = "Selected Components"

class RecommendedComponents(models.Model):
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
        verbose_name_plural = "Recommended Components"

class OpenLoopAnalysisEquations(models.Model):
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
        verbose_name = "Open-Loop Analysis Equation"
        verbose_name_plural = "Open-Loop Analysis Equations"