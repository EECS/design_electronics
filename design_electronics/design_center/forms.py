from django import forms
from .models import DCDC
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import StrictButton

class DesignParamForm(forms.Form):
    '''
    Creates a form for the design parameter portion of the
    power electronics portion of the website. Takes one input
    argument, must be passed the DCDC converter object parameters to create
    the form completely.
    '''

    def __init__(self, data = None, *args, **kwargs):
        super(DesignParamForm, self).__init__(data, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        #Loop through all parameters to be used
        #to build the form.
        for param in args[0]:
            #Param list will be a comma separated, two entry
            #string with the abbreviation as the first entry
            #and the full parameter name as the second entry.
            parsed_param = str(param).split(",")
            abbrev_param = parsed_param[0].strip()
            field_name = parsed_param[1].strip().capitalize()
            self.fields[field_name] = forms.DecimalField(required=True, min_value=0.001, decimal_places=2)