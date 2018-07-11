from django import forms

DESIGN_PARAM_LIST = ["Fs", "Io", "RipIo", "RipVo", "VD1", "Vin", "Vo"]

class DesignParamForm(forms.Form):
    '''
    Creates a form for the design parameter portion of the
    power electronics portion of the website. Takes one input
    argument, must be passed the DCDC converter object parameters to create
    the form completely.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Loop through all parameters to be used
        #to build the form.
        for param in args[0]:
            #Param list will be a comma separated, two entry
            #string with the abbreviation as the first entry
            #and the full parameter name as the second entry.
            parsed_param = str(param).split(",")
            field_name = parsed_param[0].strip()

            self.fields[field_name] = forms.DecimalField(required=True, min_value=0.001, decimal_places=2)
            #print(field_name)
    
    def clean(self):
        for param in DESIGN_PARAM_LIST:
            if self.cleaned_data.get(param):
                clean_val = self.cleaned_data[param]
                if param  == "RipIo" and self.cleaned_data["Io"] < clean_val:
                    self.add_error(param, "Value cannot be lower than output current.")
                elif param  == "RipVo" and self.cleaned_data["Vo"] < clean_val:
                    self.add_error(param, "Value cannot be lower than output voltage.")
    
    def get_fields(self):
        for field_name in self.fields:
            yield self[field_name]
