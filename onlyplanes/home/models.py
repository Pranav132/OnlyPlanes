from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Airline(models.Model):
    iataCode = models.TextField()
    icaoCode = models.TextField()
    name = models.TextField()

class Airport(models.Model):
    iataCode = models.TextField()
    city = models.TextField()
    country = models.TextField()
    continent = models.TextField()

class Segment(models.Model):
    segment_id = models.TextField()
    flightNumber = models.TextField()
    origin = models.TextField()
    originTerminal = models.TextField()
    departureTime = models.TextField()
    destination = models.TextField()
    destinationTerminal = models.TextField()
    arrivalTime = models.TextField()
    duration = models.TextField()

class OutboundLeg(models.Model):
    segments = models.ManyToManyField(Segment)

class ReturnLeg(models.Model):
    segments = models.ManyToManyField(Segment)

class Booking(models.Model):
    seats_available = models.TextField()
    price = models.TextField()
    travelClass = models.TextField()
    outboundLeg = models.ManyToManyField(OutboundLeg)
    returnLeg = models.ManyToManyField(ReturnLeg)
    user = models.ForeignKey(User, null=True, on_delete=CASCADE)

class HotelCategories(models.Model):
 
   name = models.CharField("Hotel Category Name", max_length=50)
  
   def __str__(self):
       return self.name
 
class RoomCategories(models.Model):
 
   name = models.CharField("Room Category Name", max_length=50)
  
   def __str__(self):
       return self.name
 
class Amenities(models.Model):
 
   name = models.CharField("Amenity Name", max_length=50)
  
   def __str__(self):
       return self.name
 
 
 
class Room(models.Model):
   roomcategory = models.ForeignKey(RoomCategories, on_delete=CASCADE)
   hotelcategory = models.ForeignKey(HotelCategories, on_delete=CASCADE)
   price =  models.DecimalField(
       "Price", default=0.00, max_digits=10, decimal_places=2)
   available_rooms = models.IntegerField("availability")
   max_occupancy = models.IntegerField("occupants")
   amenities = models.ManyToManyField(Amenities)

 
 
class Hotel(models.Model):
   name = models.CharField("Hotel name", max_length = 100, blank = False)
  
   exterior_picture = models.ImageField(
       "Image 1",
       upload_to='images/',
       height_field=None,
       width_field=None,
       max_length=100,
   )
   cheaproom_picture = models.ImageField(
       "Image 2",
       upload_to='images/',
       height_field=None,
       width_field=None,
       max_length=100,
   )
   mediumroom_picture = models.ImageField(
       "Image 3",
       upload_to='images/',
       height_field=None,
       width_field=None,
       max_length=100,
   )
   expensiveroom_picture = models.ImageField(
       "Image 4",
       upload_to='images/',
       height_field=None,
       width_field=None,
       max_length=100,
   )
 
   category = models.ForeignKey(HotelCategories, on_delete=CASCADE)
   location = models.CharField("Hotel city name", max_length = 50, blank = False)
   detailed_address = models.TextField("Hotel detailed address", blank = False)
   description = models.TextField("Hotel description", blank = False)
   cheaproom_name = models.CharField("cheap room  name", max_length = 50, blank = False)
   middleroom_name = models.CharField("middle room  name", max_length = 50, blank = False)
   expensiveroom_name = models.CharField("expensive room  name", max_length = 50, blank = False)
   starrating = models.IntegerField("Rating", default=1, validators=[
       MaxValueValidator(5), MinValueValidator(1)],
       null=False, blank=False)
    

class Aircraft(models.Model):
    iataCode = models.CharField(max_length=3)
    icaoCode = models.CharField(max_length=4)
    name = models.TextField()

class ReviewsRatings(models.Model):

    # includes a user foreign key and project foreign key, not null, to link who has reviewed which product
    # has a rating which cannot be null, validated for a range of 1 to 5 (will be stars)
    # has a review field which can be blank, as some people may just rate and not review

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, null=False, on_delete=models.CASCADE)
    rating = models.IntegerField("Rating", default=1, validators=[
        MaxValueValidator(5), MinValueValidator(1)],
        null=False, blank=False)
    review = models.CharField("Review", max_length=250, blank=True, null=True)








