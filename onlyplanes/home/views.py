from django.shortcuts import render, redirect
from .handler import findFlights, makeBooking

# Create your views here.

# view for main page


def index(request):
    return render(request, 'index.html')


def flight_search(request):

    context = {}
    
    if request.GET['originLocationCode'] and request.GET['destinationLocationCode'] and request.GET['departureDate']:
        kwargs = {'max': 5 }

        for i in request.GET:
            kwargs[i] = request.GET[i]

        context['trip_offers'] = findFlights(**kwargs)

        #to save a trip as a booking model:
        trip = context['trip_offers'][0]
        #makeBooking(trip)


    return render(request, "flight_search.html", context=context)










#with open("home/airport-codes.csv", "r") as file:
        #reader = csv.reader(file)
        #next(reader)
        #for row in reader:
            #City,Country ,Code,Continent
            #Airport.objects.create(iataCode = row[2], city = (row[0] if "Airport" in row[0] else row[0] + " Aiport").replace("+", ","), country = row[1].replace("+", ","), continent= row[3])
