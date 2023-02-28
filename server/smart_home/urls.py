from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename="user")
router.register('devices', views.DeviceViewSet, basename="device")
router.register('user_devices', views.UserDeviceViewSet, basename="userdevice")
router.register('homes', views.HomeViewSet, basename="home")
router.register('rooms', views.RoomViewSet, basename="room")

urlpatterns = [
    path('', include(router.urls))
]
