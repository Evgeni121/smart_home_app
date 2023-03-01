from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Device, HomeDevice, RoomDevice, Home, Room
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query = {}
        for key in self.request.query_params.keys():
            query[key] = self.request.query_params.get(key)
        if self.request.query_params:
            try:
                return User.objects.filter(**query)
            except User.DoesNotExist:
                pass
        else:
            return User.objects.all().order_by('-date_joined')


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all().order_by('name')
    serializer_class = serializers.DeviceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HomeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = {}
        for key in self.request.query_params.keys():
            query[key] = self.request.query_params.get(key)
        if self.request.query_params:
            try:
                return Home.objects.filter(**query)
            except Home.DoesNotExist:
                pass
        else:
            return Home.objects.all().order_by('name')


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('name')
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class HomeDeviceViewSet(viewsets.ModelViewSet):
    queryset = HomeDevice.objects.all().order_by('device')
    serializer_class = serializers.HomeDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomDeviceViewSet(viewsets.ModelViewSet):
    queryset = RoomDevice.objects.all().order_by('device')
    serializer_class = serializers.RoomDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
