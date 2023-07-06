from django.contrib import admin
from .models import *

# TO make models visible in admin panel
admin.site.register(Elevator)
admin.site.register(ElevatorRequest)