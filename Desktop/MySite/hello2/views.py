from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def hello_world(request):
    return render(request, "index.html")


def hello_world2(request):
    return render(request, "index2.html")


def hello_world3(request):
    return render(request, "index3.html")
