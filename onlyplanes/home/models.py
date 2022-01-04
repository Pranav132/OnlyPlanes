from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

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



