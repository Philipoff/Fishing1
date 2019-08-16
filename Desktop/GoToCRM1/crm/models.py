from django.db import models
from django import forms
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.CharField(max_length=100)
    about = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, null=True)
    room = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    about = models.TextField(max_length=255, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)\


    def __str__(self):
        return self.name + " " + self.surname


class RegisterValidation(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)


class LoginValidation(forms.Form):
    login = forms.CharField(max_length=30)
    password = forms.CharField(min_length=6)


class Comment(models.Model):
    name = models.CharField(max_length=30, null=True)
    text = models.TextField(max_length=255, null=True)
    target = models.IntegerField(null=True)