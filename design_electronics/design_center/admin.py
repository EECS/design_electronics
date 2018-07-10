from django.contrib import admin
from .models import DCDC
from .models import DesignParamChoices


# Register your models here.
admin.site.register(DesignParamChoices)
admin.site.register(DCDC)
