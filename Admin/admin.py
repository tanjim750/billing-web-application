from django.contrib import admin
from . import models

admin.site.register(models.Customer)
admin.site.register(models.Booking)
admin.site.register(models.MonthlyPayment)
admin.site.register(models.Logo)