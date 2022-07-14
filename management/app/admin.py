from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Timeslot)
admin.site.register(Specialists)
admin.site.register(Appointment)
admin.site.register(TakeAppointment)
admin.site.register(Credentials)
