import pathlib
import csv
from django.shortcuts import render, redirect
from .models import Aircraft, Airline, Airport, Hotel, Room
from .handler import findFlights, makeBooking

# Create your views here.

# view for main page


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def hotels(request):
    hotels = Hotel.objects.all()
    print(hotels)
    return render(request, 'hotels.html', {"hotels": hotels})


def search(request):

    airport_instances = Airport.objects.all().order_by('city')

    airports = []
    for airport_instance in airport_instances:
        airports = airports[:] + [airport_instance.__dict__]
    for airport in airports:
        airport['city'] = str(airport['city'])[
            :-7].replace("International", "").replace(" Int'l", "")

    context = {
        'airports': airports,
        'search_details': request.GET,
    }

    if request.GET.get('originLocationCode', None) and request.GET.get('destinationLocationCode', None) and request.GET.get('departureDate', None):
        kwargs = {'max': 50}

        for i in request.GET:
            if request.GET[i] != "" and request.GET[i] != 0:
                kwargs[i] = request.GET[i]
        kwargs.pop('searchType')
        print(kwargs)

        context['trip_offers'] = findFlights(**kwargs)

        # to save a trip as a booking model:
        # makeBooking(trip)

    print(len(airports))

    return render(request, "search_page/search.html", context=context)


# with open("home/airport-codes.csv", "r") as file:
    #reader = csv.reader(file)
    # next(reader)
    # for row in reader:
    #City,Country ,Code,Continent
    #Airport.objects.create(iataCode = row[2], city = (row[0] if "Airport" in row[0] else row[0] + " Aiport").replace("+", ","), country = row[1].replace("+", ","), continent= row[3])
