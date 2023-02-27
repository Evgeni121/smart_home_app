import requests
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Device, Home, Room, HomeDevice, RoomDevice
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = serializers.HomeSerializer
    permission_classes = [permissions.IsAuthenticated]


class HomeDeviceViewSet(viewsets.ModelViewSet):
    queryset = HomeDevice.objects.all()
    serializer_class = serializers.HomeDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomDeviceViewSet(viewsets.ModelViewSet):
    queryset = RoomDevice.objects.all()
    serializer_class = serializers.RoomDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
