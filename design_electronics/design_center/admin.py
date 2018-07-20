from django.contrib import admin
from .models import DCDC, DesignParamChoices, DCDCRecommendedComponents, DCDCSelectedComponents


# Register your models here.
admin.site.register(DesignParamChoices)
admin.site.register(DCDC)
admin.site.register(DCDCRecommendedComponents)
admin.site.register(DCDCSelectedComponents)
