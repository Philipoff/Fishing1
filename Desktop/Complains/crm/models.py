from django.db import models
from django import forms
# Create your models here.


class Problem(models.Model):
    name = models.CharField(max_length=63, null=True)
    creator = models.TextField(max_length=30, null=True)
    about = models.TextField(max_length=255, null=True)
    closed = models.TextField(null=True)
    room = models.IntegerField(null=True)
    helper = models.TextField(max_length=30, null=True)

    def __str__(self):
        return self.name


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