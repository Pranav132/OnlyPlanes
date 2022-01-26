from django.contrib import admin
from .models import *

admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Segment)
admin.site.register(OutboundLeg)
admin.site.register(ReturnLeg)
admin.site.register(FlightBooking)
admin.site.register(HotelCategories)
admin.site.register(RoomCategories)
admin.site.register(Amenities)
admin.site.register(Room)
admin.site.register(Hotel)
admin.site.register(Aircraft)
admin.site.register(ReviewsRatings)
admin.site.register(HotelBooking)

# Register your models here.
