from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from django_jinja import library
import jinja2

def crispy(form):
    return as_crispy_form(form, 'Bootstrap3', form.helper.label_class, form.helper.field_class)

jinja2.filters.FILTERS['crispy'] = crispy