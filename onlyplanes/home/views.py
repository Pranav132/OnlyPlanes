import pathlib
import csv
from unicodedata import category
from black import re
from django.shortcuts import render, redirect
from .models import *
from .handler import findFlights, makeBooking
from .forms import *
from django.db.models import Q
from datetime import datetime
# from urllib.parse import unquote

# Create your views here.

# view for main page


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def hotels(request):
    if request.method == 'GET':
        hotels = Hotel.objects.all()
        rooms = Room.objects.filter(roomcategory=2)

        filter_form = FilterForm(
            initial={'name': 'high2low', 'price': 'zero', 'rating': 'none'})

        return render(request, 'hotels.html', {"hotels": hotels, 'rooms': rooms, 'filter_form': filter_form})

    # If form for sorting and filtering is submitted, we need to display the hotels in a particular way.
    if request.method == 'POST':

        # getting all the required values from the form
        name = request.POST.get('name')
        price = request.POST.get('price')
        rating = request.POST.get('rating')

        # returning Filter Form with the selected parameters
        filter_form = FilterForm(
            initial={'name': name, 'price': price, 'rating': rating})

        # Now, we will do filtering first, and then do sorting

        # FILTERS

        # Check all values
        print("THE NAME IS: ", name)
        print("THE PRICE IS: ", price)
        print("THE RATING IS: ", rating)

        max_price = 0.00
        min_price = 0.00

        # assign value to min_price and max_price
        if price == 'zero':
            max_price = 100000.00
            min_price = 0.00
        elif price == 'one':
            max_price = 9999.00
            min_price = 1000.00
        elif price == 'ten':
            max_price = 20000.00
            min_price = 10000.00

        print(min_price)
        print(max_price)

        max_rating = 5.00
        min_rating = 0.00

        # assign value to min_rating

        if rating == 'none':
            min_rating = 0.00
        elif rating == 'five':
            min_rating = 5.00
        elif rating == 'four':
            min_rating = 4.00
        elif rating == 'three':
            min_rating = 3.00
        elif rating == 'two':
            min_rating = 2.00
        elif rating == 'one':
            min_rating = 1.00

        print(min_rating)
        print(max_rating)

        unsorted_hotels = Hotel.objects.all()
        room = Room.objects.filter(roomcategory=2)

        # The idea is to filter the rooms by price and then filter the rooms based on only those which have the same hotel
        # category as the hotels in unsorted_hotels so that we have hotels of a particular rating and THEN of a particular
        # price range.

        unsorted_rooms = room.filter(
            Q(price__gte=min_price),
            Q(price__lte=max_price),
        )

        unsorted_hotels = unsorted_hotels.filter(
            Q(starrating__gte=min_rating),
            Q(starrating__lte=max_rating),
        )

        print("THE 3 STAR HOTELS BEFORE LIST ARE: ",
              unsorted_hotels.filter(starrating=3))

        # making a list of all the hotel categories in the unsorted_hotels hotels
        hotelCategoryList = []
        roomHotelCategoryList = []

        for hotel in unsorted_hotels:
            if hotel.category in hotelCategoryList:
                continue
            else:
                hotelCategoryList.append(hotel.category)

        for room in unsorted_rooms:
            if room.hotelcategory in roomHotelCategoryList:
                continue
            else:
                roomHotelCategoryList.append(room.hotelcategory)

        print("HOTEL", hotelCategoryList)
        print("ROOM", roomHotelCategoryList)

        # Now, we have all rooms within the price range required, and a list of the hotel categories to choose from
        # We need to filter the rooms based on the hotel categories.

        rooms = unsorted_rooms.filter(hotelcategory__in=hotelCategoryList)
        hotels = unsorted_hotels.filter(category__in=roomHotelCategoryList)
        print(rooms)
        print(hotels)

        # Since hotel category is directly related to room prices, sorting according to hotel category would give us a reliable
        # sorting method.
        # High to low and low to high.

        economy_hotels = hotels.filter(category=3)
        # print("ECONOMY HOTELS: ", economy_hotels)
        boutique_hotels = hotels.filter(category=2)
        # print("BOUTIQUE HOTELS: ", boutique_hotels)
        luxury_hotels = hotels.filter(category=1)
        # print("LUXURY HOTELS: ", luxury_hotels)

        if name == 'low2high':
            hotels = economy_hotels | boutique_hotels | luxury_hotels
        elif name == 'high2low':
            hotels = luxury_hotels | boutique_hotels | economy_hotels

        return render(request, 'hotels.html', {"hotels": hotels, 'rooms': rooms, 'filter_form': filter_form})


def hotel_search(request):

    if request.method == 'GET':
        search = request.GET['searched']
        print("THE SEARCH TERM IS: ", search)
        rooms = Room.objects.filter(roomcategory=2)

        filter_form = FilterForm(
            initial={'name': 'high2low', 'price': 'zero', 'rating': 'none'})

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

        return render(request, 'hotel_search.html', {"hotels": hotels, 'rooms': rooms, 'filter_form': filter_form, 'search_term': search})

    if request.method == 'POST':
        search = request.POST.get('searched')
        print("THE SEARCH TERM IS: ", search)
        rooms = Room.objects.filter(roomcategory=2)

        filter_form = FilterForm(
            initial={'name': 'high2low', 'price': 'zero', 'rating': 'none'})

        # Primary search term will be location mostly, nobody searches using Hotel name
        # We need to accommodate for people putting in hotel names also, in case they don't listen to the placeholder text
        # Other than that, there is no such requirement that can be searched for, the rest will be in the sorting and filtering forms

        location_search = Hotel.objects.filter(location__icontains=search)
        name_search = Hotel.objects.filter(name__icontains=search)

        unsorted_hotel = location_search | name_search

        # getting all the required values from the form
        name = request.POST.get('name')
        price = request.POST.get('price')
        rating = request.POST.get('rating')

        # returning Filter Form with the selected parameters
        filter_form = FilterForm(
            initial={'name': name, 'price': price, 'rating': rating})

        # Now, we will do filtering first, and then do sorting

        # FILTERS

        # Check all values
        print("THE NAME IS: ", name)
        print("THE PRICE IS: ", price)
        print("THE RATING IS: ", rating)

        max_price = 0.00
        min_price = 0.00

        # assign value to min_price and max_price
        if price == 'zero':
            max_price = 100000.00
            min_price = 0.00
        elif price == 'one':
            max_price = 9999.00
            min_price = 1000.00
        elif price == 'ten':
            max_price = 20000.00
            min_price = 10000.00

        print(min_price)
        print(max_price)

        max_rating = 5.00
        min_rating = 0.00

        # assign value to min_rating

        if rating == 'none':
            min_rating = 0.00
        elif rating == 'five':
            min_rating = 5.00
        elif rating == 'four':
            min_rating = 4.00
        elif rating == 'three':
            min_rating = 3.00
        elif rating == 'two':
            min_rating = 2.00
        elif rating == 'one':
            min_rating = 1.00

        print(min_rating)
        print(max_rating)

        unsorted_hotels = unsorted_hotel
        room = Room.objects.filter(roomcategory=2)

        # The idea is to filter the rooms by price and then filter the rooms based on only those which have the same hotel
        # category as the hotels in unsorted_hotels so that we have hotels of a particular rating and THEN of a particular
        # price range.

        unsorted_rooms = room.filter(
            Q(price__gte=min_price),
            Q(price__lte=max_price),
        )

        unsorted_hotels = unsorted_hotels.filter(
            Q(starrating__gte=min_rating),
            Q(starrating__lte=max_rating),
        )

        # making a list of all the hotel categories in the unsorted_hotels hotels
        hotelCategoryList = []
        roomHotelCategoryList = []

        for hotel in unsorted_hotels:
            if hotel.category in hotelCategoryList:
                continue
            else:
                hotelCategoryList.append(hotel.category)

        for room in unsorted_rooms:
            if room.hotelcategory in roomHotelCategoryList:
                continue
            else:
                roomHotelCategoryList.append(room.hotelcategory)

        print("HOTEL", hotelCategoryList)
        print("ROOM", roomHotelCategoryList)

        # Now, we have all rooms within the price range required, and a list of the hotel categories to choose from
        # We need to filter the rooms based on the hotel categories.

        rooms = unsorted_rooms.filter(hotelcategory__in=hotelCategoryList)
        hotels = unsorted_hotels.filter(category__in=roomHotelCategoryList)
        print(rooms)
        print(hotels)

        # Since hotel category is directly related to room prices, sorting according to hotel category would give us a reliable
        # sorting method.
        # High to low and low to high.

        economy_hotels = hotels.filter(category=3)
        boutique_hotels = hotels.filter(category=2)
        luxury_hotels = hotels.filter(category=1)

        if name == 'low2high':
            hotels = economy_hotels | boutique_hotels | luxury_hotels
        elif name == 'high2low':
            hotels = luxury_hotels | boutique_hotels | economy_hotels

        return render(request, 'hotel_search.html', {"hotels": hotels, 'rooms': rooms, 'filter_form': filter_form, 'search_term': search})

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

    # hotel reviews
    ratings = ReviewsRatings.objects.filter(hotel=hotel_id).all()

    return render(request, 'eachhotel.html', {"hotel": hotel, 'rooms': rooms, 'hotel_reccos': reccos, 'ratings': ratings, 'user': request.user})


def search(request):

    # offerdetails = request.POST.get('offerdetails')
    # if offerdetails:
    #     print('lol')
    #     print(offerdetails)
    #     print('lol')
    #     return render(request, 'flight_booking.html', {'offer': offerdetails})

    airport_instances = Airport.objects.all().order_by('city')

    airports = []
    for airport_instance in airport_instances:
        airports = airports[:] + [airport_instance.__dict__]
    for airport in airports:
        airport['city'] = str(airport['city'])[
            :-7].replace("International", "").replace(" Int'l", "")

    try:
        context = {
            'airports': airports,
            'search_details': request.GET,
            'people': request.GET['adults'],
            'origin': request.GET['originLocationCode'],
            'destination': request.GET['destinationLocationCode'],
            'departureDate': request.GET['departureDate']
        }
    except:
        context = {
            'airports': airports,
            'search_details': request.GET,
        }

    if request.GET.get('originLocationCode', None) and request.GET.get('destinationLocationCode', None) and request.GET.get('departureDate', None):
        kwargs = {'max': 25}

        for i in request.GET:
            if request.GET[i] != "" and request.GET[i] != 0:
                kwargs[i] = request.GET[i]
        print(kwargs)

        context['trip_offers'] = findFlights(**kwargs)
        print("find flights done")

        # to save a trip as a booking model:
        # makeBooking(trip)

    # print(len(airports))

    airport_instances = Airport.objects.all().order_by('city')

    airports = []
    for airport_instance in airport_instances:
        airports = airports[:] + [airport_instance.__dict__]
    for airport in airports:
        airport['city'] = str(airport['city'])[
            :-7].replace("International", "").replace(" Int'l", "")

    return render(request, "search.html", context=context)

    # with open("home/airport-codes.csv", "r") as file:
    # reader = csv.reader(file)
    # next(reader)
    # for row in reader:
    # City,Country ,Code,Continent
    # Airport.objects.create(iataCode = row[2], city = (row[0] if "Airport" in row[0] else row[0] + " Aiport").replace("+", ","), country = row[1].replace("+", ","), continent= row[3])


def flight_booking(request):

    if request.method == 'GET':

        params = request.GET['offer']
        params += '\'}'

        print("\n\n\n\n\n")
        print(params)
        print("\n\n\n\n\n")

        people = request.GET['people']
        origin = request.GET['origin']
        destination = request.GET['destination']
        departureDate = request.GET['departureDate']
        # people --  HAVE
        # price -- HAVE
        # cabinClass
        # DepartureLocation  -- HAVE
        # departureDate -- HAVE
        # arrivalLocation -- HAVE

        price = ""

        for i in range(params.index('price')+9, len(params)):
            if params[i] == ' ':
                break
            else:
                price += params[i]

        cabinClass = ""

        for i in range(params.index('travelClass')+15, len(params)):
            if params[i] == '\'':
                break
            else:
                cabinClass += params[i]

        context = {
            # people --  HAVE
            # price -- HAVE
            # cabinClass
            # DepartureLocation  -- HAVE
            # departureDate -- HAVE
            # arrivalLocation -- HAVE
            'people': int(people),
            'price': float(price),
            'cabinClass': cabinClass,
            'departureDate': departureDate,
            'destination': destination,
            'origin': origin,
        }

        return render(request, 'flight_booking.html', context=context)

    if request.method == 'POST':

        context = {
            'booking_flight': True,
            'people': int(request.POST.get('people')),
            'price': (request.POST.get('price')),
            'cabinClass': request.POST.get('cabinClass'),
            'departureDate': request.POST.get('departureDate'),
            'destination': request.POST.get('destination'),
            'origin': request.POST.get('origin'),
        }
        print(context)
        return render(request, 'checkout.html', context=context)


def hotel_booking(request, hotel_id, room_id, room_name):
    if request.method == 'GET':
        hotel = Hotel.objects.get(id=hotel_id)
        room = Room.objects.get(id=room_id)
        roomname = room_name

        booking_form = BookingForm()

        context = {
            'hotel': hotel,
            'room': room,
            'roomname': roomname,
            'booking_form': booking_form,
        }

        return render(request, 'hotel_booking.html', context=context)

    if request.method == 'POST':
        context = {
            'booking_hotel': True,
            'date_from': request.POST.get('date_from'),
            'date_to': request.POST.get('date_to'),
            'rooms': int(request.POST.get('rooms')),
            'guests': int(request.POST.get('guests')),
            'hotel': Hotel.objects.get(id=hotel_id),
            'room': Room.objects.get(id=room_id),
            'roomname': room_name,
        }

        if context['guests']/context['rooms'] > 2:
            hotel = Hotel.objects.get(id=hotel_id)
            room = Room.objects.get(id=room_id)

            booking_form = BookingForm()

            context = {
                'hotel': hotel,
                'room': room,
                'booking_form': booking_form,
                'message': "Number of guests per room should be 2 or below."
            }

            return render(request, 'hotel_booking.html', context=context)
        else:
            context = {
                'booking_hotel': True,
                'date_from': request.POST.get('date_from'),
                'date_to': request.POST.get('date_to'),
                'rooms': int(request.POST.get('rooms')),
                'guests': int(request.POST.get('guests')),
                'hotel': Hotel.objects.get(id=hotel_id),
                'room': Room.objects.get(id=room_id),
                'roomname': room_name,
            }
            return render(request, 'checkout.html', context=context)


def checkout(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        if room_id:
            room_selected = Room.objects.get(id=room_id)
            checkInDate = request.POST.get('checkInDate')
            checkOutDate = request.POST.get('checkOutDate')
            user = request.user
            hotel_id = request.POST.get('hotel_id')
            hotel = Hotel.objects.get(id=hotel_id)
            guests = int(request.POST.get('guests'))
            price = float(request.POST.get('price'))
            rooms = int(request.POST.get('rooms'))
            print(rooms)
            numberOfNights = 4

            for i in range(0, rooms):
                booking = HotelBooking(
                    checkInDate=checkInDate,
                    checkOutDate=checkOutDate,
                    user=user,
                    hotel=hotel,
                    room_selected=room_selected,
                    numberOfGuests=guests,
                    totalPrice=price,
                    numberOfNights=numberOfNights
                )
                HotelBooking.save(booking)
                print('MADE ONE ROOM BOOKING')

            context = {
                'message': "You're all set for a good time!"
            }

            return redirect('index')
        else:
            people = int(request.POST.get('people'))
            price = float(request.POST.get('price'))
            cabinClass = request.POST.get('cabinClass')
            departureDate = request.POST.get('departureDate')
            destination = request.POST.get('destination')
            origin = request.POST.get('origin')

            departureDate = datetime.fromisoformat(departureDate).date()
            print(departureDate)

            for i in range(0, people):
                booking = bookingFlight(
                    people=people,
                    price=price,
                    cabinClass=cabinClass,
                    departureDate=departureDate,
                    arrivalLocation=destination,
                    DepartureLocation=origin,
                    user=request.user,

                )
                bookingFlight.save(booking)
                print("BOOKED ONE SEAT ON FLIGHT")

            context = {
                'message': "You're all set for a good time!"
            }

            return redirect('index')


def newreview(request, hotel_id):
    if request.method == "POST":
        review = request.POST.get('review')
        hotel = Hotel.objects.get(id=hotel_id)
        new_review = ReviewsRatings.objects.create(
            user=request.user, hotel=hotel, rating=10, review=review)
        new_review.save()
        return redirect('eachhotel', hotel_id=hotel_id)

    if request.method == "GET":
        hotel = Hotel.objects.get(id=hotel_id)
        return render(request, "new_review.html", {"hotel": hotel})


def deleteReview(request, reviewsRatings_id):
    review = ReviewsRatings.objects.filter(id=reviewsRatings_id)
    print(review)
    # if delete button posted
    if request.method == "POST":
        hotel_id = request.POST.get("hotel_id")
        review.delete()
        # deleting review
        return redirect('eachhotel', hotel_id=hotel_id)
