#Use crispy forms for form rendering
from crispy_forms.utils import render_crispy_form
from django_jinja import library
from jinja2 import contextfunction
from django import template

register = template.Library()

@contextfunction
@library.global_function
def crispy(context, form):
    return render_crispy_form(form, context=context)