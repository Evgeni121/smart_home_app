from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename="user")
router.register('devices', views.DeviceViewSet, basename="device")
router.register('device_prop', views.DevicePropertiesViewSet, basename="deviceproperties")
router.register('homes', views.HomeViewSet, basename="home")
router.register('rooms', views.RoomViewSet, basename="room")
router.register('home_devices', views.HomeDeviceViewSet, basename="homedevice")
router.register('room_devices', views.RoomDeviceViewSet, basename="roomdevice")

urlpatterns = [
    path('', include(router.urls))
]
