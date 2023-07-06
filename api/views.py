from django.shortcuts import render,HttpResponse, redirect
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def elevators(request,count=None):
    if not count:
        return HttpResponse(json.dumps([i.serialize for i in Elevator.objects.all()]))
    ids = []
    for i in range(count):
        data = Elevator()
        data.save()
        ids.append(data.id)
    return HttpResponse(json.dumps(f'{count} elevators generated ids: {ids}'))

def get_nearby_lift(floor):
    lis1 = []
    for ele in Elevator.objects.filter(operational=True):
        dic = {}
        if ele.available_status == 'available':
            try:
                ab = ElevatorRequest(elevator=ele,request_floor=floor)
                ab.save()
                ele.running_status = 'start'
                ele.save()
                return ele.id
            except Exception as e:
                print('error-1',e)

        else:
            diff = floor - ele.current_floor
            dic['lift'] = ele.serialize
            dic['distance'] = diff
            dic['requested_floors'] = ele.get_requested_floors()
            lis1.append(dic) 

    lis2 = sorted(lis1,key=lambda x:x['distance']) 
    up_plus = []
    down_plus = []
    up_minus = []
    down_minus = []
    for item in lis2:
        print(item)
        if item['distance'] > 0:
            if item['lift']['direction'] == 'up':
                dic = {}
                dic['lift'] = item['lift']['id']
                dic['distance'] = item['distance']
                up_plus.append(dic)
            elif item['lift']['direction'] == 'down':
                dic = {}
                dic['lift'] = item['lift']['id']
                dic['distance'] = item['lift']['current_floor'] * 2 + item['distance']
                down_plus.append(dic)
        elif item['distance'] < 0:
            if item['lift']['direction'] == 'down':
                dic = {}
                dic['lift'] = item['lift']['id']
                dic['distance'] = -(item['distance'])
                down_minus.append(dic)
            elif item['lift']['direction'] == 'up':
                dic = {}
                dic['lift'] = item['lift']['id']
                item['requested_floors'].sort(reverse=True)
                top_floor = item['requested_floors'][0]
                current_floor = item['lift']['current_floor']
                dic['distance'] = (top_floor - current_floor) + (top_floor - floor)
                up_minus.append(dic)
        elif item['distance'] == 0:
            try:
                ele = Elevator.objects.get(id=item['lift']['id'])
                ab = ElevatorRequest(elevator=ele,request_floor=floor)
                ab.save()
                return ele.id
            except Exception as e:
                print('error-2',e)


    final_list = []
    up_plus_2 = sorted(up_plus,key=lambda x:x['distance'])
    down_plus_2 = sorted(down_plus,key=lambda x:x['distance'])
    down_minus_2 = sorted(down_minus,key=lambda x:x['distance'])
    up_minus_2 = sorted(up_minus,key=lambda x:x['distance'])
    if up_plus_2:
        final_list.append(up_plus_2[0])
    if down_plus_2:
        final_list.append(down_plus_2[0])
    if down_minus_2:
        final_list.append(down_minus_2[0])
    if up_minus_2:
        final_list.append(up_minus_2[0])

    final_list_2 = sorted(final_list,key=lambda x:x['distance'])
    _lift = None
    if final_list_2:
        _lift = final_list_2[0]['lift']
   
    if _lift:
        try:
            ele = Elevator.objects.get(id=_lift)
            ab = ElevatorRequest(elevator=ele,request_floor=floor)
            ab.save()
            return ele.id
        except Exception as e:
            print('error-3',e)

def move(request):
    all_lifts = Elevator.objects.filter(operational=True)
    for lift in all_lifts:
        next_floors = sorted(lift.get_requested_floors())
        if next_floors:
            next_floor = next_floors[0]
            if next_floor > lift.current_floor:
                lift.direction = 'up'
                lift.available_status = 'busy'
                lift.current_floor +=1
            elif next_floor < lift.current_floor:
                lift.direction = 'down'
                lift.available_status = 'busy'
                lift.current_floor -=1
            elif next_floor == lift.current_floor:
                a = ElevatorRequest.objects.get(request_floor=next_floor)
                a.delete()
                                
        else:
            if lift.current_floor > 0:
                lift.direction = 'down'
                lift.available_status = 'available' 
                lift.current_floor -= 1
            elif lift.current_floor == 0:
                lift.available_status = 'available'
                lift.direction = 'ideal'
                lift.running_status = 'stop'
        lift.save()
    return HttpResponse(json.dumps([i.serialize for i in Elevator.objects.filter(operational=True)]))

def elevator_not_working(request,id):
    try:
        ele = Elevator.objects.get(id=id)
        ele.operational = False
        ele.save()
        return HttpResponse(json.dumps(f'Elevator {ele.id} status updated to not working.'))
    except:
        ids = [i.id for i in Elevator.objects.all()]
        return HttpResponse(f'Elevator with this id: {id} not found. Available elevators: {ids}')

@csrf_exempt
def elevator(request,id):
    try:
        ele = Elevator.objects.get(id=id)
    except:
        ids = [i.id for i in Elevator.objects.all()]
        return HttpResponse(f'Elevator with this id: {id} not found. Available elevators: {ids}')

    if request.method == 'POST':
        door_status = request.POST.get('door_status','')
        if door_status:
            if door_status == 'open':
                ele.door_status = 'open'
                return HttpResponse(f'Door Status Updated for elevator: {ele.id} to : Open')
            elif door_status == 'close':
                ele.door_status = 'close'
                return HttpResponse(f'Door Status Updated for elevator: {ele.id} to : Close')
            else:
                return HttpResponse('Invalid Request')

        return HttpResponse('Invalid Request')
    else:
        return HttpResponse(json.dumps(ele.serialize)) 
    

def request_elevator(request,floor):
    if floor == 0:
        return HttpResponse(f'Already at ground floor.')
    try:
        ele = ElevatorRequest.objects.get(request_floor=floor).elevator
        return HttpResponse(f'Already assigned to lift: {ele.id}')
    except Exception as e:
        ele = get_nearby_lift(floor)
        return HttpResponse(f'Floor {floor} assigned to lift: {ele}')