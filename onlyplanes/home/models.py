from django.db import models

# Create your models here.

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


