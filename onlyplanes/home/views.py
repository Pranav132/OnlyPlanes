from django.shortcuts import render, redirect
from .handler import findFlights

# Create your views here.

# view for main page


def index(request):
    return render(request, 'index.html')

def flight_search(request):
    if request.GET :
        kwargs = {'max' : 5}
        for i in request.GET:
            kwargs[i] = request.GET[i]
        print(kwargs)
        findFlights(**kwargs)

    return render(request, "flight_search.html")
