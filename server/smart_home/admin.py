from django.contrib import admin

from .models import Device, Home, Room, HomeDevice, RoomDevice

admin.site.register(Device)
admin.site.register(Home)
admin.site.register(Room)
admin.site.register(HomeDevice)
admin.site.register(RoomDevice)
