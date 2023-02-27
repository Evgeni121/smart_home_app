from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('devices', views.DeviceViewSet)
router.register('homes', views.HomeViewSet)
router.register('home_devices', views.HomeDeviceViewSet)
router.register('rooms', views.RoomViewSet)
router.register('room_devices', views.RoomDeviceViewSet)

urlpatterns = [
    path('', include(router.urls))
]
