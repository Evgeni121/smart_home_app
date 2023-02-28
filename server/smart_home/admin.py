from django.contrib import admin

from .models import Device, UserDevice, Home, Room

admin.site.register(Device)
admin.site.register(UserDevice)
admin.site.register(Home)
admin.site.register(Room)

