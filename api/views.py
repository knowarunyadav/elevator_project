from django.shortcuts import HttpResponse
from .utils import *
from .models import Elevator, ElevatorRequest
import sys
import json

def elevators(request, count=None):
    '''
    This api is used to get the details of the elevators .
    :param:count:None
    :return: JSON.
    '''

    if not count:
        return HttpResponse(json.dumps([i.serialize for i in Elevator.objects.all()]))

    '''
    This api can be used to create elevators
    :param: count: Number of Elevators you want you create
    :return: Will return the ids of the elevators created.
    '''

    ids = []
    for i in range(count):
        ele = Elevator()
        ele.save()
        ids.append(ele.id)
    return HttpResponse(json.dumps(f'{count} elevators generated ids: {ids}'))




def move(request):
    '''
    This Api is used to move the eles by one step ahead,i.e one step up or down
    based on to the requested floor and open/close door.
    :return: JSON | details of evelator after movement.
    '''

    eles = Elevator.objects.filter(operational=True)
    if not eles:
        return HttpResponse(f'No elevators available.')

    for ele in eles:
        move_next_floor(ele)

    return HttpResponse(json.dumps([i.serialize for i in Elevator.objects.filter(operational=True)]))

def elevator_not_working(request,id):
    '''
    Set an elevator to non-operational
    :return: str : status updated.
    '''

    try:
        ele = Elevator.objects.get(id=id)
        ele.operational = False
        ele.save()
        return HttpResponse(json.dumps(f'Elevator {ele.id} status updated to not working.'))
    except:
        ids = [i.id for i in Elevator.objects.all()]
        return HttpResponse(f'Elevator with this id: {id} not found. Available elevators: {ids}')

def elevator(request,id):
    '''
    Will provide the details for a particular elevator, its direction, avaiilable status
    doors open/close,current floor and next floors request.
    return : json
    '''

    try:
        ele = Elevator.objects.get(id=id)
        return HttpResponse(json.dumps(ele.serialize)) 
    except:
        ids = [i.id for i in Elevator.objects.all()]
        return HttpResponse(f'Elevator with this id: {id} not found. Available elevators: {ids}')

    

def request_elevator(request,floor):
    '''
    Main Api to call the elevator from a particular floor
    :param:floor: Floor Number
    :return: elevator id to which the floor is assigned.
    '''

    if floor == 0:
        # cannot Request from Ground Floor, since drop floor
        # is always ground floor for each request by default
        return HttpResponse(f'Already at ground floor.')
    try:
        # Same floor cannot be requested twice since a elevator
        # is already assigned.
        ele = ElevatorRequest.objects.get(request_floor=floor).elevator
        return HttpResponse(f'Already assigned to ele: {ele.id}')
    except Exception as e:
        try:
            ele = get_nearby_ele(floor)
            if not ele:
                # in case all elevators are non functional .
                return HttpResponse(f'NO elevators available.')
            return HttpResponse(f'Floor {floor} assigned to ele: {ele}')
        except Exception as e:
            print(f'Error: {e} | line: {sys.exc_info()[2].tb_lineno}')
            