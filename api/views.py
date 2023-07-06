from django.shortcuts import HttpResponse
from .models import Elevator, ElevatorRequest
import json
import sys

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


def get_plus_up(ele,floor):
    dic = {}
    dic['ele'] = ele['ele']['id']
    current_floor = ele['ele']['current_floor']
    top_floor = sorted(ele['ele']['next_floors_requested'],reverse=True)
    if top_floor:
        top_floor = top_floor[0]
        if top_floor > floor:
            main_floor = top_floor
        else:
            main_floor = floor
        distance = (main_floor - current_floor)+main_floor
        dic['distance'] = distance
    else:
        dic['distance'] = ele['distance']*2+current_floor
    dic['status'] = ele['ele']['available_status']
    dic['count'] = len(ele['ele']['next_floors_requested'])
    return dic

def get_plus_down(ele,floor):
    dic = {}
    dic['ele'] = ele['ele']['id']
    dic['distance'] = ele['ele']['current_floor'] * \
        2 + ele['distance']
    dic['status'] = ele['ele']['available_status']
    dic['count'] = len(ele['ele']['next_floors_requested'])
    return dic

def get_minus_down(ele,floor):
    dic = {}
    dic['ele'] = ele['ele']['id']
    dic['distance'] = -(ele['distance'])
    dic['status'] = ele['ele']['available_status']
    dic['count'] = len(ele['ele']['next_floors_requested'])
    return dic

def get_minus_up(ele,floor):
    dic = {}
    dic['ele'] = ele['ele']['id']
    ele['requested_floors'].sort(reverse=True)
    try:
        top_floor = ele['requested_floors'][0]
    except:
        top_floor = None
    current_floor = ele['ele']['current_floor']
    if top_floor:
        dic['distance'] = (top_floor - current_floor) + \
                        (top_floor - floor)
    else:
        dic['distance'] = current_floor - floor

    dic['status'] = ele['ele']['available_status']
    dic['count'] = len(ele['ele']['next_floors_requested'])
    return dic

def get_min_ele_time(ele_status,floor):
    ele_status = sorted(ele_status, key=lambda x: x['distance'])
    plus_up = []
    plus_down = []
    minus_up = []
    minus_down = []
    for ele in ele_status:
        if ele['distance'] > 0:
            if ele['ele']['direction'] == 'up' or ele['ele']['direction'] == 'ideal':
                ele_time = get_plus_up(ele,floor)
                plus_up.append(ele_time)
            
            elif ele['ele']['direction'] == 'down':
                ele_time = get_plus_down(ele,floor)               
                plus_down.append(ele_time)
                
        elif ele['distance'] < 0:
            if ele['ele']['direction'] == 'down':
                ele_time = get_minus_down(ele,floor)
                minus_down.append(ele_time)
            
            elif ele['ele']['direction'] == 'up':
                ele_time = get_minus_up(ele,floor)
                minus_up.append(ele_time)
        
        elif ele['distance'] == 0 and ele['ele']['direction'] == 'down':
            try:
                ele = Elevator.objects.get(id=ele['ele']['id'])
                ab = ElevatorRequest(elevator=ele, request_floor=floor)
                ab.save()
                return ele.id
            except Exception as e:
                print(f'Error: {e} | line: {sys.exc_info()[2].tb_lineno}')
        

    min_ele_time = []

    plus_up = sorted(plus_up, key=lambda x: (x['distance'],x['status'],x['count']))
    plus_down = sorted(plus_down, key=lambda x: (x['distance'],x['status'],x['count']))
    minus_down = sorted(minus_down, key=lambda x: (x['distance'],x['status'],x['count']))
    minus_up = sorted(minus_up, key=lambda x: (x['distance'],x['status'],x['count']))
    if plus_up:
        min_ele_time.append(plus_up[0])
    if plus_down:
        min_ele_time.append(plus_down[0])
    if minus_down:
        min_ele_time.append(minus_down[0])
    if minus_up:
        min_ele_time.append(minus_up[0])

    min_ele_time = sorted(min_ele_time, key=lambda x: x['distance'])
    return min_ele_time

def get_nearby_ele(floor):
    ele_status = []
    for ele in Elevator.objects.filter(operational=True):
        dic = {}
        diff = floor - ele.current_floor
        dic['ele'] = ele.serialize
        dic['distance'] = diff
        dic['requested_floors'] = ele.get_requested_floors()
        ele_status.append(dic)

    min_ele_time = get_min_ele_time(ele_status,floor)
 
    if isinstance(min_ele_time,int):
        return min_ele_time
 
    if isinstance(min_ele_time,list):
        _ele = min_ele_time[0]['ele']
        try:
            ele = Elevator.objects.get(id=_ele)
            if ele.available_status == 'available' and ele.direction == 'ideal':
                ele.running_status = 'start'
                ele.available_status = 'busy'
                ele.direction = 'up'
                ele.save()

            ab = ElevatorRequest(elevator=ele, request_floor=floor)
            ab.save()
            return ele.id
        except Exception as e:
            print(f'Error: {e} | line: {sys.exc_info()[2].tb_lineno}')

    # Need to check this code required or not !!!
    '''
    else:
        _ele = None

    if _ele:
        try:
            ele = Elevator.objects.get(id=_ele)
            if ele.available_status == 'available' and ele.direction == 'ideal':
                ele.running_status = 'start'
                ele.available_status = 'busy'
                ele.direction = 'up'
                ele.save()

            ab = ElevatorRequest(elevator=ele, request_floor=floor)
            ab.save()
            return ele.id
        except Exception as e:
            print(f'Error: {e} | line: {sys.exc_info()[2].tb_lineno}')
    else:
        for ele in Elevator.objects.filter(operational=True):
            dic = {}
            if ele.available_status == 'available' and ele.direction == 'ideal':
                try:
                    ab = ElevatorRequest(elevator=ele, request_floor=floor)
                    ab.save()
                    ele.running_status = 'start'
                    ele.available_status = 'busy'
                    ele.direction = 'up'
                    ele.save()
                    return ele.id
                except Exception as e:
                    print(f'Error: {e} | line: {sys.exc_info()[2].tb_lineno}')

    '''

def move_next_floor(ele):
    try:
        current_floor = ele.current_floor
        direction = ele.direction
        next_floors = ele.get_requested_floors()
        next_floor = 0
        if next_floors:
            if direction == 'up':
            # If the ele is going Upwards we will 
            # check the next floor in Up direction
                temp_next_floor = sorted(
                    [i for i in next_floors if i >= current_floor])
                
                try:
                    next_floor = temp_next_floor[0]
                except:
                    # Since there are no more requests from top floors,
                    #  the ele needs to change change direction and go down
                    ele.direction = 'down'
                    ele.save()
                    return

            elif direction == 'down':
                # We will check the next floor requested while going down.
                temp_next_floor = sorted(
                    [i for i in next_floors if i <= current_floor], reverse=True)
                try:
                    next_floor = temp_next_floor[0]
                except:
                    # if there's no request while going down then, definitely it will move towards Ground Floor 
                    next_floor = 0

            if next_floor > ele.current_floor:
                # Move one floor Up
                ele.direction = 'up'
                ele.available_status = 'busy'
                ele.door = 'close'
                ele.running_status = 'start'
                ele.current_floor += 1
                ele.save()
            elif next_floor < ele.current_floor:
                # Move one floor Down
                ele.direction = 'down'
                ele.available_status = 'busy'
                ele.door = 'close'
                ele.running_status = 'start'
                ele.current_floor -=1
                ele.save()
            elif next_floor == ele.current_floor == 0:
                # since it has more pending floors which we have checked above
                # and it's at ground floor it should vacate and and go up.
                ele.direction = 'up'
                ele.running_status = 'stop'
                ele.door = 'open'
                ele.save()
            elif next_floor == ele.current_floor:
                # Since it's reached it's destinated floor, will remove the request now.
                ele.running_status = 'stop'
                ele.door = 'open'
                ele.save()
                a = ElevatorRequest.objects.get(request_floor=next_floor)
                a.delete()
                                
        else:
            # if there are no more floor's request pending, it can move to ground floor
            if ele.current_floor > 0:
                ele.direction = 'down'
                ele.available_status = 'busy' 
                ele.door = 'close'
                ele.running_status = 'start'
                ele.current_floor -= 1

            elif ele.current_floor == 0:
                # If already at Ground Floor
                ele.available_status = 'available'
                ele.direction = 'ideal'
                ele.door = 'close'
                ele.running_status = 'stop'
        ele.save()
    except Exception as e:
        print(f'Error: {e} | line: {sys.exc_info()[2].tb_lineno}')


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
            