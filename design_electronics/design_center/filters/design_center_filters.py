from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from django.template import Context
import jinja2

def crispy(form):
    c = Context({
            'formset': form,
            'form_show_errors': True,
            'form_show_labels': True,
            'label_class': form.helper.label_class,
            'field_class': form.helper.field_class,
        })

    return form.helper.render_layout(form, c, 'bootstrap3')

jinja2.filters.FILTERS['crispy'] = crispy