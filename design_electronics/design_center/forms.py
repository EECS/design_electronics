from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

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
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-designParamForm'

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

        #Capitalize label of each field in the form.
        self.helper.label_class = 'col-lg-6 title-case'
        self.helper.field_class = 'col-lg-6 align-right'
        
        self.helper.layout = Layout()

        for field in self.fields:
            self.helper.layout.append(
                Field(field, wrapper_class="flex-space-between"),
            )

    #Accepts arguments power electronics circuit type, smps circuit type, dcdc type and circuit name.
    def custom_clean(self, pe_ct, smps_ct, dcdc_ct, ct_name):
        cleaned_data = self.cleaned_data
        
        if len(cleaned_data) > 0:
            
            #Convert to Fs input parameter to kHz.
            if abbrev_design_params["Fs"] in cleaned_data:
                self.cleaned_data[abbrev_design_params["Fs"]] = self.cleaned_data[abbrev_design_params["Fs"]]*1000
            
            if str(pe_ct) == "SMPS":
                if str(smps_ct) == "DCDC":
                    if str(dcdc_ct) == "CCM":
                        
                        #Ripple current cannot be larger than output current in a CCM converter.
                        if (self.cleaned_data[abbrev_design_params["Io"]] <= 
                                self.cleaned_data[abbrev_design_params["RipIo"]]):
                            self.add_error(abbrev_design_params["RipIo"], 
                                "Output ripple current cannot be equal to or greater than output current.")

                        #Ripple voltage cannot be larger than output voltage in a CCM converter.
                        if (self.cleaned_data[abbrev_design_params["Vo"]] <= 
                            self.cleaned_data[abbrev_design_params["RipVo"]]):
                            self.add_error(abbrev_design_params["RipVo"], 
                                "Output ripple voltage cannot be equal to or greater than output voltage.")
                        
                        #BUCK CONVERTER ERRORS
                        if str(ct_name) == "Buck Converter":

                            #Output Voltage cannot be greater than input voltage in a buck converter.
                            if (self.cleaned_data[abbrev_design_params["Vo"]] >= 
                                self.cleaned_data[abbrev_design_params["Vin"]]):
                                self.add_error(abbrev_design_params["Vin"], 
                                    "Input voltage cannot be less than or equal to output voltage in a buck converter.")


class DesignCompForm(forms.Form):
    '''
    Creates a form for the selected components portion of the
    power electronics portion of the website. Takes one input
    argument, must be passed the DCDC converter object parameters to create
    the form completely.
    '''

    def __init__(self, data = None, *args, **kwargs):
        super(DesignCompForm, self).__init__(data, *args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-designCompForm'

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
        
        #Capitalize label of each field in the form.
        self.helper.label_class = 'col-lg-6 title-case'
        self.helper.field_class = 'col-lg-6 align-right'

        self.helper.layout = Layout()

        for field in self.fields:
            self.helper.layout.append(
                Field(field, wrapper_class="flex-space-between"),
            )

    #Accepts arguments power electronics circuit type, smps circuit type, dcdc type and circuit name.
    def custom_clean(self, pe_ct, smps_ct, dcdc_ct, ct_name):
        cleaned_data = self.cleaned_data
        
        if len(cleaned_data) > 0:
            
            #Convert to Fs input parameter to kHz
            if "Fs" in abbrev_component_params and abbrev_component_params["Fs"] in cleaned_data.values():
                self.cleaned_data[abbrev_design_params["Fs"]] = cleaned_data[abbrev_design_params["Fs"]]*1000

            for k in cleaned_data.copy().keys():
                if self.cleaned_data[k] < 0:
                    self.add_error(k, "Parameters cannot be less than 0.")

                if "capacitor" in k.lower() or "inductor" in k.lower():
                    self.cleaned_data[k] = self.cleaned_data[k]/1000000