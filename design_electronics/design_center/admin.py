from django.contrib import admin
from .models import DCDC, DesignParamChoices, DCDCRecommendedComponents, DCDCSelectedComponents, DCDCOpenLoopAnalysisEquations


# Register your models here.
admin.site.register(DesignParamChoices)
admin.site.register(DCDC)
admin.site.register(DCDCRecommendedComponents)
admin.site.register(DCDCSelectedComponents)
admin.site.register(DCDCOpenLoopAnalysisEquations)
