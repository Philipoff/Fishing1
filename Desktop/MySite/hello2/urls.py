from django.urls import path
from hello2 import views

urlpatterns = [
    path('', views.hello_world, name='hello'),
    path('', views.hello_world2, name='Stilee.css'),
    path('', views.hello_world3, name='hello3')
]

