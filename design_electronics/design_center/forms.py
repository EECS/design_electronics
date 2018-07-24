from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

abbrev_design_params = {}
abbrev_component_params = {}

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
        self.helper.form_id = 'id-designParamForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.layout = Layout(
            Div(
                Div('field1', css_class="col-xs-6"),
                Div('field3', css_class='col-xs-6'),
                css_class='row-fluid'), 
            )

        #Loop through all parameters to be used
        #to build the form.
        for param in args[0]:
            #Param list will be a comma separated, two entry
            #string with the abbreviation as the first entry
            #and the full parameter name as the second entry.
            parsed_param = str(param).split(",")
            abbrev_param = parsed_param[0].strip()
            field_name = parsed_param[1].strip().title()

            abbrev_design_params.update({abbrev_param:field_name})

            self.fields[field_name] = forms.DecimalField(required=True, min_value=0.001)

            if "voltage" in field_name.lower():
                self.fields[field_name].help_text = "V"
            elif "current" in field_name.lower():
                self.fields[field_name].help_text = "A"
            elif "frequency" in field_name.lower():
                self.fields[field_name].help_text = "kHz"
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        if len(cleaned_data) > 0:
            #Convert to Fs input parameter to kHz
            self.cleaned_data[abbrev_design_params["Fs"]] = self.cleaned_data[abbrev_design_params["Fs"]]*1000
        #    if self.cleaned_data[abbrev_design_params["Io"]] <= self.cleaned_data[abbrev_design_params["RipIo"]]:
        #        self.add_error(abbrev_design_params["RipIo"], "Value cannot be equal to or lower than output current.")
        #    
        #    if self.cleaned_data[abbrev_design_params["Vo"]] < self.cleaned_data[abbrev_design_params["RipVo"]]:
        #        self.add_error(abbrev_design_params["RipVo"], "Value cannot be equal to or lower than than output voltage.")

class DesignCompForm(forms.Form):
    '''
    Creates a form for the selected components portion of the
    power electronics portion of the website. Takes one input
    argument, must be passed the DCDC converter object parameters to create
    the form completely.
    '''

    def __init__(self, data = None, *args, **kwargs):
        super(DesignCompForm, self).__init__(data, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-designCompForm'
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
            field_name = parsed_param[1].strip().title()

            abbrev_component_params.update({abbrev_param:field_name})

            self.fields[field_name] = forms.DecimalField(required=True)

            if "capacitor" in field_name.lower():
                self.fields[field_name].help_text = "microFarads"
            elif "inductor" in field_name.lower():
                self.fields[field_name].help_text = "microHenries"
            elif "resistance" in field_name.lower():
                self.fields[field_name].help_text = "Ohms"
            elif "voltage" in field_name.lower():
                self.fields[field_name].help_text = "V"
            elif "current" in field_name.lower():
                self.fields[field_name].help_text = "A"
            elif "frequency" in field_name.lower():
                self.fields[field_name].help_text = "kHz"

    def clean(self):
        cleaned_data = self.cleaned_data
        
        if len(cleaned_data) > 0:
            #Convert to Fs input parameter to kHz
            self.cleaned_data[abbrev_params["Fs"]] = self.cleaned_data[abbrev_params["Fs"]]*1000
        #    if self.cleaned_data[abbrev_params["Io"]] <= self.cleaned_data[abbrev_params["RipIo"]]:
        #        self.add_error(abbrev_params["RipIo"], "Value cannot be equal to or lower than output current.")
        #    
        #    if self.cleaned_data[abbrev_params["Vo"]] < self.cleaned_data[abbrev_params["RipVo"]]:
        #        self.add_error(abbrev_params["RipVo"], "Value cannot be equal to or lower than than output voltage.")