from django.shortcuts import render, redirect

from .models import Booking, OutboundLeg, ReturnLeg, Segment
from .handler import findFlights

# Create your views here.

# view for main page


def index(request):
    return render(request, 'index.html')


def flight_search(request):
    if request.GET:
        kwargs = {'max': 5}
        for i in request.GET:
            kwargs[i] = request.GET[i]
        print(kwargs)
        response = findFlights(**kwargs)
        trip = response[0]
        outboundLeg = OutboundLeg.objects.create()
        returnLeg = ReturnLeg.objects.create()

        for segment in trip['outboundLeg']:
            outboundLeg.segments.add(Segment.objects.create(**segment))


        trip.pop('outboundLeg')

        print(trip)

        for key in trip:
            if key == 'returnLeg':
                for segment in trip['returnLeg']:
                    returnLeg.segments.add(Segment.objects.create(**segment))
                trip.pop(key)

        current_booking = Booking.objects.create(**trip)
        current_booking.outboundLeg.add(outboundLeg)
        current_booking.returnLeg.add(returnLeg)


    return render(request, "flight_search.html")
