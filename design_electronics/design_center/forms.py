from django import forms

class DesignParamForm(forms.ModelForm):
    class Meta:
        model = DesignParamChoices