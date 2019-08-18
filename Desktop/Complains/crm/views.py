from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from crm.models import Problem
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from crm.models import *


# Основная страница
def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    problems = Problem.objects.all().exclude(closed='on')
    return render(request, 'index.html', {'problems': problems})


# Функция просмотра информации о жалобе
def details(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'GET':
        id = request.GET.get('id')
        problem = Problem.objects.get(pk=id)
        return render(request, 'details.html', {'problem': problem})

    if request.method == 'POST':
        id = request.GET.get('id')
        problem = Problem.objects.get(pk=id)
        return redirect('/problem?id={}'.format(problem.id))


# Функция добавления жалобы
def add(request):
    if request.method == 'GET':
        problems = Problem.objects.all()
        return render(request, 'add.html', {'problems': problems})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        room = request.POST.get('room', '')
        about = request.POST.get('about', '')
        creator = request.user

        if name == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/add')

        problem = Problem()
        problem.name = name
        problem.room = room
        problem.about = about
        problem.creator = creator
        like = Like()
        like.save()
        problem.likes = like
        problem.save()

        return redirect('/problem?id={}'.format(problem.id))


def logout_page(request):
    logout(request)
    return redirect('/login')


def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginValidation(request.POST)
        if not form.is_valid():
            return HttpResponse('Заполните данные корректно!')

        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return HttpResponse('Неверные данные!')
        login(request, user)
        return redirect('/')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterValidation(request.POST)
        if not form.is_valid():
            return HttpResponse('Заполните все поля!')

        user = User()
        user.username = request.POST.get('login')
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password'))
        user.save()

        login(request, user)

        return redirect('/')


def myproblems(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    problems = Problem.objects.all().filter(creator=request.user)
    return render(request, 'myproblems.html', {'problems': problems})


def edit(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    problem = Problem.objects.get(pk=id)
    if request.method == 'GET':
        return render(request, 'edit.html', {'problem': problem})

    if request.method == 'POST':
        helper = request.POST.get('helper')
        closed = request.POST.get('closed')

        problem.helper = helper
        problem.closed = closed
        problem.save()

        return redirect('/problem?id={}'.format(problem.id))


def panel(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.is_superuser:
        return HttpResponse('Вы не имеете прав!')
    problems = Problem.objects.all().exclude(closed='on')
    problems1 = Problem.objects.all().filter(helper=request.user).exclude(closed='on')
    return render(request, 'panel.html', {'problems': problems, 'problems1': problems1})


def archive(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    problems = Problem.objects.all().filter(closed='on')
    return render(request, 'archive.html', {'problems': problems})


def makelike(request):
    id = request.GET.get('id')
    if request.user.is_authenticated:
        user_tags = User.objects.filter(likedone=id)
        current_user = request.user
        if current_user not in user_tags:
            try:
                like = Like.objects.get(id=id)
                like.thumbnumber += 1
                like.likedone.add(current_user)
                like.save()
                return redirect('/problem?id={}'.format(id))
            except ObjectDoesNotExist:
                return redirect('/problem?id={}'.format(id))
        else:
            return redirect('/problem?id={}'.format(id))
    else:
        return redirect('/problem?id={}'.format(id))
