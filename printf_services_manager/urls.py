from django.urls import path
from . import views


app_name = 'manager'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('services', views.services, name='services'),
]
