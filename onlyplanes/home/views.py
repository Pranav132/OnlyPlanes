from django.shortcuts import render, redirect

# Create your views here.

# view for main page


def index(request):
    return render(request, 'index.html')
