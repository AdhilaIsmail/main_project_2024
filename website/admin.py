from django.contrib import admin
from . import models


admin.site.register(models.CustomUser)
admin.site.register(models.Donor)
admin.site.register(models.DonorResponse)
admin.site.register(models.HospitalRegister)
admin.site.register(models.BloodRequest)
admin.site.register(models.Payment)


