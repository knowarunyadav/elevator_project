from django.db import models
from django.utils import timezone

class Elevator(models.Model):
    direction = models.CharField(max_length=64,choices=(('up','up'),('down','down'),('ideal','ideal')),default='ideal')
    door = models.CharField(max_length=64,choices=(('open','open'),('close','close')),default='close')
    running_status = models.CharField(max_length=64,choices=(('start','start'),('stop','stop')),default='stop')
    available_status = models.CharField(max_length=64,choices=(('available','available'),('busy','busy')),default='available')
    operational = models.BooleanField(default=True)
    created = models.DateTimeField(null=True,blank=True)
    current_floor = models.IntegerField(default=0)
    

    def save(self,*args,**kwargs):
        if not self.id:
            self.created = timezone.now()
        super(Elevator, self).save(*args, **kwargs)
    
    @property
    def serialize(self):
        dic = {}
        dic['id'] = self.id
        dic['direction'] = self.direction
        dic['door'] = self.door
        dic['running_status'] = self.running_status
        dic['current_floor'] = self.current_floor
        dic['available_status'] = self.available_status
        dic['operational'] = self.operational
        dic['next_floors_requested'] = self.get_requested_floors()
        return dic

    def get_requested_floors(self):
        return [i.__dict__['request_floor'] for i in ElevatorRequest.objects.filter(elevator=self)]

class ElevatorRequest(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    request_count = models.IntegerField(default=0)
    request_floor = models.IntegerField(default=0,unique=True)
    created = models.DateTimeField(null=True,blank=True)

    def save(self,*args,**kwargs):
        if not self.id:
            self.created = timezone.now()
        super(ElevatorRequest, self).save(*args, **kwargs)

    @property
    def serialize(self):
        dic = {}
        dic['id'] = self.id
        dic['elevator'] = self.elevator.id
        dic['request_count'] = self.request_count
        dic['request_floor'] = self.request_floor
        dic['created'] = str(self.created)
        return dic
