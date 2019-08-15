from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "index3.html")


def page(request):
    return render(request, "index2.html")


def settings(request):
    return render(request, "index3.html")
