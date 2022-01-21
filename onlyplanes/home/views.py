import pathlib
import csv
from django.shortcuts import render, redirect
from .models import Aircraft, Airline, Airport, Hotel, Room
from .handler import findFlights, makeBooking
from .forms import *

# Create your views here.

# view for main page


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def hotels(request):
    hotels = Hotel.objects.all()
    rooms = Room.objects.filter(roomcategory=2)

    return render(request, 'hotels.html', {"hotels": hotels, 'rooms': rooms})


def hotel_search(request):

    if request.method == 'GET':
        search = request.GET['searched']
        rooms = Room.objects.filter(roomcategory=2)

        # Primary search term will be location mostly, nobody searches using Hotel name
        # We need to accommodate for people putting in hotel names also, in case they don't listen to the placeholder text
        # Other than that, there is no such requirement that can be searched for, the rest will be in the sorting and filtering forms

        location_search = Hotel.objects.filter(location__icontains=search)
        name_search = Hotel.objects.filter(name__icontains=search)

        unsorted_hotel = location_search | name_search

        hotels = []

        for hotel in unsorted_hotel:
            if hotel in hotels:
                continue
            else:
                hotels.append(hotel)

        # form for sorting and filtering to be put here

    return render(request, 'hotels.html', {"hotels": hotels, 'rooms': rooms})

    # # initializing the form and setting the default value to be relevance
    # filter_form = FilterForm(
    #     initial={'name': 'relevance', 'price': 'zero', 'gender': 'none', 'types': 'nothing', 'use': 'useless'})
    # return render(request, 'product_search.html', {"product": product, "search": search, "filter_form": filter_form})


def eachhotel(request, hotel_id):
    all_hotels = Hotel.objects.all()
    hotel = Hotel.objects.filter(id=hotel_id).first()
    rooms = Room.objects.filter(hotelcategory=hotel.category)
    print(hotel.location)

    # hotel reccommendations based on the location of the hotel in question
    reccos = Hotel.objects.filter(location=hotel.location).exclude(id=hotel_id)
    return render(request, 'eachhotel.html', {"hotel": hotel, 'rooms': rooms, 'hotel_reccos': reccos})


def search(request):

    if request.method == 'POST':

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

        # print(len(airports))

        return render(request, "search.html", context=context)

    elif request.method == 'GET':

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
        return render(request, "search.html", context=context)

        # with open("home/airport-codes.csv", "r") as file:
        #reader = csv.reader(file)
        # next(reader)
        # for row in reader:
        #City,Country ,Code,Continent
        #Airport.objects.create(iataCode = row[2], city = (row[0] if "Airport" in row[0] else row[0] + " Aiport").replace("+", ","), country = row[1].replace("+", ","), continent= row[3])
