from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from crm.models import Student, Course
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from crm.models import *


# Основная страница
def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        students = Student.objects.all().filter(name__icontains=search_term)
    else:
        students = Student.objects.all()
    return render(request, 'index.html', {'students': students})


# Функция просмотра информации об ученике
def details(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'GET':
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        comments = Comment.objects.filter(target=student.id).order_by('-id')
        return render(request, 'details.html', {'comments': comments, 'student': student})

    if request.method == 'POST':
        text = request.POST.get('text', '')
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        target = student.id
        comment = Comment()
        comment.name = request.user
        comment.text = text
        comment.target = target
        comment.save()
        return redirect('/student?id={}'.format(student.id))


# Функция добавления ученика
def add(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, 'add.html', {'courses': courses})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        course_id = request.POST.get('course_id', '')
        room = request.POST.get('room', '')
        email = request.POST.get('email', '')
        about = request.POST.get('about', '')

        if name == '' or surname == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/add')

        student = Student()
        student.name = name
        student.surname = surname
        student.room = room
        student.email = email
        student.about = about

        if course_id != '':
            course = Course.objects.get(pk=course_id)
            student.course = course
        else:
            student.course = None
        student.save()

        return redirect('/student?id={}'.format(student.id))


# Функция редактирования информации об ученике
def edit(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'GET':
        id = request.GET.get('id')
        # Импорт информации из базы данных
        courses = Course.objects.all()
        student = Student.objects.get(pk=id)

        return render(request, 'edit.html', {'student': student, 'courses': courses})

    if request.method == 'POST':
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        course_id = request.POST.get('course_id', '')
        room = request.POST.get('room', '')
        email = request.POST.get('email', '')
        about = request.POST.get('about', '')
        id = request.GET.get('id')

        if name == '' or surname == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/add')

        student = Student.objects.get(pk=id)
        student.name = name
        student.surname = surname
        student.room = room
        student.email = email
        student.about = about

        if course_id != '':
            course = Course.objects.get(pk=course_id)
            student.course = course
        else:
            student.course = None
        student.save()
        return redirect('/student?id={}'.format(student.id))


def delete(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    student = Student.objects.get(pk=id)
    student.delete()

    return redirect('/')


def courses(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def course(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    course = Course.objects.get(pk=id)
    return render(request, 'course.html', {'course': course})


def addcourse(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, 'addcourse.html', {'courses': courses})

    if request.method == 'POST':
        name = request.POST.get('name', '')
        teacher = request.POST.get('teacher', '')
        about = request.POST.get('about', '')

        if name == '' or teacher == '' or about == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/addcourse')

        course = Course()
        course.name = name
        course.teacher = teacher
        course.about = about
        course.save()

        return redirect('/course?id={}'.format(course.id))


def editcourse(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        id = request.GET.get('id')
        course1 = Course.objects.get(pk=id)
        return render(request, 'editcourse.html', {'course': course1})

    if request.method == 'POST':
        id = request.GET.get('id')
        course1 = Course.objects.get(pk=id)

        name = request.POST.get('name', '')
        teacher = request.POST.get('teacher', '')
        about = request.POST.get('about', '')

        course1.name = name
        course1.teacher = teacher
        course1.about = about
        course1.save()

        return redirect('/course?id={}'.format(course1.id))


# Регистрация и авторизация пользователя

def secret(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'index.html')


def logout_page(request):
    logout(request)
    return redirect('/login')


def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginValidation(request.POST)
        if not form.is_valid():
            return HttpResponse('Заполните все поля!')

        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return HttpResponse('Неверные данные!')
        else:
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


