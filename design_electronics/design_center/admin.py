from django.contrib import admin
from .models import DCDC, DesignParamChoices, DCDCRecommendedComponents


# Register your models here.
admin.site.register(DesignParamChoices)
admin.site.register(DCDC)
admin.site.register(DCDCRecommendedComponents)
