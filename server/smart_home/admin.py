from django.contrib import admin

from .models import Device, HomeDevice, RoomDevice, Home, Room, DeviceProperties

admin.site.register(Device)
admin.site.register(DeviceProperties)
admin.site.register(HomeDevice)
admin.site.register(RoomDevice)
admin.site.register(Home)
admin.site.register(Room)
