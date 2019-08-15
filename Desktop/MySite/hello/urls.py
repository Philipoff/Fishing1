from django.contrib import admin
from django.urls import path
from hello.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('about', about),
    path('page', page),
    path('settings', settings)
]

