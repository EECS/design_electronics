from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

DESIGN_PARAM_LIST = ["Fs", "Io", "RipIo", "RipVo", "VD1", "Vin", "Vo"]

class DesignParamForm(forms.Form):
    '''
    Creates a form for the design parameter portion of the
    power electronics portion of the website. Takes one input
    argument, must be passed the DCDC converter object parameters to create
    the form completely.
    '''
    abbrev_params = {}

    def __init__(self, *args, **kwargs):
        super(DesignParamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-designParamForm"
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))

        #Loop through all parameters to be used
        #to build the form.
        #for param in args[0]:
        #    #Param list will be a comma separated, two entry
        #    #string with the abbreviation as the first entry
        #    #and the full parameter name as the second entry.
        #    parsed_param = str(param).split(",")
        #    abbrev_param = parsed_param[0].strip()
        #    field_name = parsed_param[1].strip()
#
        #    print(self.fields)
        #    #self.fields[field_name] = forms.DecimalField(required=True, min_value=0.001, decimal_places=2)
        #    self.abbrev_params[abbrev_param] = field_name
        #    break
        #    #print(field_name)
    
    def __str__(self):
        return str(self.helper)
    
    def clean(self):
        for param in DESIGN_PARAM_LIST:
            if self.cleaned_data.get(param):
                clean_val = self.cleaned_data[param]
                abbrev_param = self.abbrev_params[param]
                if abbrev_param  == "RipIo" and self.cleaned_data[self.abbrev_params["Io"]] < clean_val:
                    self.add_error(param, "Value cannot be lower than output current.")
                elif abbrev_param  == "RipVo" and self.cleaned_data[self.abbrev_params["Vo"]] < clean_val:
                    self.add_error(param, "Value cannot be lower than output voltage.")
    
    test_field = forms.DecimalField(required=True, min_value=0.001, decimal_places=2, label="Test Field")