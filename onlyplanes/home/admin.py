from django.contrib import admin
from .models import *

admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Segment)
admin.site.register(OutboundLeg)
admin.site.register(ReturnLeg)
admin.site.register(Booking)

# Register your models here.
