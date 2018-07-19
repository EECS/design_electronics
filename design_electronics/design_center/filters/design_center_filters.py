from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
import jinja2

def crispy(form):
    return as_crispy_form(form, 'bootstrap3', form.helper.label_class, form.helper.field_class)

jinja2.filters.FILTERS['crispy'] = crispy