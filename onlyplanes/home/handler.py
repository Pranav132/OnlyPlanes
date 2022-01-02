import json
from amadeus import Client, ResponseError
import datetime
from .models import *
import requests
amadeus = Client(
    client_id='QrdT9b97pTA0aaYGN57uUgR7u6RWlAEM',
    client_secret='4Z69ZYu2vJfGP8Ff'
)

google_search_API_key = "AIzaSyBJApYBKCxHj117n85GF1Ri3t63q0PKBtE"
# This is to query the api and get flights


def findFlights(**kwargs):
    options = []
    try:
        response = amadeus.shopping.flight_offers_search.get(
            currencyCode='INR', **kwargs)
        
        for trip in response.data:
            try: 
                trip_dict = {
                    'seats_available': trip['numberOfBookableSeats'],
                    'price': trip['price']['total'] + " " + trip['price']['currency'],
                    'travelClass': trip['travelerPricings'][0]['fareDetailsBySegment'][0]['cabin'],

                # the following entries contain the outbound and return legs. They need to be read in from a for loop. each leg contains
                # multiple 'flights', each of which is a dictionary with the attributes shown below.

                # 'outboundLeg' : [{'segment_id' : flight['id'],
                # 'flightNumber' : flight['carrierCode'] + " " + flight['number'],
                # 'origin' : flight['departure']['iataCode'],
                # 'originTerminal' : flight['departure'].get('terminal', '-'),
                # 'departureTime' : flight['departure']['at'][11:16] + " " + datetime.datetime(int(flight['departure']['at'][0:4]), int(flight['departure']['at'][5:7]), int(flight['departure']['at'][8:10])).strftime("%a, %d %b %Y"),
                # 'destination' : flight['arrival']['iataCode'],
                # 'destinationTerminal' : flight['arrival'].get('terminal', '-'),
                # 'arrivalTime' : flight['arrival']['at'][11:16] + " " + datetime.datetime(int(flight['arrival']['at'][0:4]), int(flight['arrival']['at'][5:7]), int(flight['arrival']['at'][8:10])).strftime("%a, %d %b %Y"),
                # 'duration' : flight['duration'][2:]
                # }, .{}..{}..{}.....],

                # 'returnLeg'   : [{'segment_id' : ,
                # 'flightNumber' : ,
                # 'origin' : ,
                # 'originTerminal' : ,
                # 'departureTime' :,
                # 'destination' : ,
                # 'destinationTerminal' : ,
                # 'arrivalTime' : ,
                # 'duration' :
                # }, ..{}..{}..{}.... ],
                }

            # getting the outbound and return Leg data:

                for i in range(len(trip['itineraries'])):

                    flights = []

                    for flight in trip['itineraries'][i]['segments']:

                        ORIGIN = Airport.objects.get(iataCode = flight['departure']['iataCode'])
                        DESTINATION = Airport.objects.get(iataCode = flight['arrival']['iataCode'])
                        AIRLINE = Airline.objects.get(iataCode = flight['carrierCode'])

                        flights = flights[:] + [{
                            'airline' : AIRLINE,
                            'segment_id': flight['id'],
                            'flightNumber': flight['carrierCode'] + " " + flight['number'],
                            'origin': ORIGIN,
                            'originTerminal': flight['departure'].get('terminal', '-'),
                            'departureTime': flight['departure']['at'][11:16] + " " + datetime.datetime(int(flight['departure']['at'][0:4]), int(flight['departure']['at'][5:7]), int(flight['departure']['at'][8:10])).strftime("%a, %d %b %Y"),
                            'destination': DESTINATION,
                            'destinationTerminal': flight['arrival'].get('terminal', '-'),
                            'arrivalTime': flight['arrival']['at'][11:16] + " " + datetime.datetime(int(flight['arrival']['at'][0:4]), int(flight['arrival']['at'][5:7]), int(flight['arrival']['at'][8:10])).strftime("%a, %d %b %Y"),
                            'duration': flight['duration'][2:].replace("H", "h ").replace("M", "m ")
                        }]

                    trip_dict['outboundLeg' if (i == 0) else 'returnLeg'] = flights

                options = options[:] + [trip_dict]
                print('option validated')

            except:
                print('error fetching airport data')


    except ResponseError as error:
        print(error)
    
    getAirlineLogo("Air India")

    return options

def getAirlineLogo(name):
    PARAMS = {
        'key' : google_search_API_key,
        'cx' : '6a92acc3ab711e762',
        'q' : name,
        'searchType' : 'image'
    }
    response = requests.get(url="https://www.googleapis.com/customsearch/v1", params=PARAMS)
 
    result = response.json()
    for i in result['items']:
        print(i['title'], i['link'])


def makeBooking(trip):
    if trip:
        outboundLeg = OutboundLeg.objects.create()
        returnLeg = ReturnLeg.objects.create()

        for segment in trip['outboundLeg']:
            outboundLeg.segments.add(Segment.objects.create(**segment))

        trip.pop('outboundLeg')


        for key in trip:
            if key == 'returnLeg':
                for segment in trip['returnLeg']:
                    returnLeg.segments.add(Segment.objects.create(**segment))
                trip.pop(key)

        current_booking = Booking.objects.create(**trip)
        current_booking.outboundLeg.add(outboundLeg)
        current_booking.returnLeg.add(returnLeg)
