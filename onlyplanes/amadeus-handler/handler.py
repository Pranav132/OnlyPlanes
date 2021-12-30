from amadeus import Client, ResponseError
import datetime

amadeus = Client(
    client_id='QrdT9b97pTA0aaYGN57uUgR7u6RWlAEM',
    client_secret='4Z69ZYu2vJfGP8Ff'
)

# This is to query the api and get flights


def findFlights(**kwargs):
    try:
        response = amadeus.shopping.flight_offers_search.get(currencyCode='INR', **kwargs)
        options = []
        for trip in response.data:
            trip_dict ={'id' : trip['id'],
                        'seats_available': trip['numberOfBookableSeats'],
                        'price' : trip['price']['total'] + " " + trip['price']['currency'],
                        'travelClass' : trip['travelerPricings'][0]['fareDetailsBySegment'][0]['cabin'],
                        }

            for i in range(len(trip['itineraries'])):
                flights = []

                for flight in trip['itineraries'][i]['segments']:
                    flights = flights[:] + [{
                        'id' : flight['id'],
                        'flightNumber' : flight['carrierCode'] + " " + flight['number'],
                        'origin' : flight['departure']['iataCode'],
                        'originTerminal' : flight['departure'].get('terminal', '-'),
                        'departureTime' : flight['departure']['at'][11:16] + " " + datetime.datetime(int(flight['departure']['at'][0:4]), int(flight['departure']['at'][5:7]), int(flight['departure']['at'][8:10])).strftime("%a, %d %b %Y"),
                        'destination' : flight['arrival']['iataCode'],
                        'destinationTerminal' : flight['arrival'].get('terminal', '-'),
                        'arrivalTime' : flight['arrival']['at'][11:16] + " " + datetime.datetime(int(flight['arrival']['at'][0:4]), int(flight['arrival']['at'][5:7]), int(flight['arrival']['at'][8:10])).strftime("%a, %d %b %Y"),
                        'duration' : flight['duration'][2:]
                    }]

                trip_dict['outboundLeg' if (i == 0) else 'returnLeg'] = flights

            options = options[:] + [trip_dict]

            for key in trip_dict:
                if key == 'outboundLeg' or key == 'returnLeg':
                    print(key, " :")
                    for segment in trip_dict[key]:
                        for i in segment:
                            print("     ", i, " : ", segment[i])
                        print("     ", "--"*20)
                else:
                    print(key, " : ", trip_dict[key], "\n")

            print('\n', "---"*20)
        
            
    except ResponseError as error: 
        print(error)

    return


findFlights(originLocationCode='DEL', destinationLocationCode='BLR',
            departureDate='2022-01-01', adults=1, max=5, returnDate = '2022-01-10')
