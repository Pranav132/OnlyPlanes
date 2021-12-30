from amadeus import Client, ResponseError

amadeus = Client(
    client_id='QrdT9b97pTA0aaYGN57uUgR7u6RWlAEM',
    client_secret='4Z69ZYu2vJfGP8Ff'
)

# This is to query the api and get flights


def findFlights(**kwargs):
    try:
        response = amadeus.shopping.flight_offers_search.get(**kwargs)
        responsedict = {}
        for trip in response.data:
            # for key in trip:
            #     if key != 'itineraries':
            #         print(key, ": ", trip[key], "\n")
            print()
            print()
            print('ID', trip['id'])
            # printing ID just to number flights

            # to get number of flights in trip
            # print("\nSEGMENTS:\n")
            for sector in trip['itineraries']:
                print(len(sector['segments']))
                # this is the number of connecting flights to get to point A from B
                for flight in sector['segments']:
                    print(flight)
                    # details of each flight in the connection
                print("\n")
            print('\n', "---"*20)

    except ResponseError as error:
        print(error)

    return


findFlights(originLocationCode='JFK', destinationLocationCode='LHR',
            departureDate='2022-01-01', adults=1, max=5)
