"""elevator_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

app_name = "api"

urlpatterns = [

    # This api can be used to create elevators
    # :param: count: Number of Elevators you want you create
    # :return: Will return the ids of the elevators created.
    path('elevators/<int:count>/', elevators,name='set_elevators'),

    # This api is used to get the details of the elevators .
    # :param:count:None
    # :return: JSON.
    path('elevators/', elevators,name='get_elevators'),

    # This Api is used to move the elevator by one step ahead,i.e one step up or down
    # based on to the requested floor and open/close door.
    # :return: JSON | details of evelator after movement.
    path('move/', move,name='move'),

    # Will provide the details for a particular elevator, its direction, avaiilable status
    # doors open/close,current floor and next floors request.
    # return : json
    path('elevator/<int:id>/', elevator,name='elevator'),

    # Set an elevator to non-operational
    # :return: str : status updated.
    path('elevator/not_working/<int:id>/', elevator_not_working,name='not_working'),

    # Main Api to call the elevator from a particular floor
    # :param:floor: Floor Number
    # :return: elevator id to which the floor is assigned.
    path('request_elevator/<int:floor>/', request_elevator,name='request_elevator'),

]
