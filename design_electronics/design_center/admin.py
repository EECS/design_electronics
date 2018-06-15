from django.contrib import admin
from .models import PowerElectronics
from .models import SMPS
from .models import DCDC


# Register your models here.
admin.site.register(PowerElectronics)
admin.site.register(SMPS)
admin.site.register(DCDC)
