from django.db import models
from django import forms
from django.contrib.auth.models import User
# Create your models here.


class Like(models.Model):
    thumbnumber = models.IntegerField(default=0, help_text="Начинается с 0", verbose_name="Число лайков")
    likedone = models.ManyToManyField(User, related_name='users_like_main', null=None)


class Problem(models.Model):
    name = models.CharField(max_length=63, null=True)
    creator = models.TextField(max_length=30, null=True)
    about = models.TextField(max_length=255, null=True)
    closed = models.TextField(null=True)
    room = models.IntegerField(null=True)
    helper = models.TextField(max_length=30, null=True)
    likes = models.ForeignKey(Like, default=0, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class RegisterValidation(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)


class LoginValidation(forms.Form):
    login = forms.CharField(max_length=30)
    password = forms.CharField(min_length=6)
