import requests
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Device, UserDevice, Home, Room
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.query_params:
            try:
                return User.objects.get(username=self.request.query_params["username"])
            except User.DoesNotExist:
                pass
        else:
            return User.objects.all().order_by('-date_joined')

    # def get_queryset(self):
    #     queryset = User.objects.all()
    #     print(self.request.query_params)
    #     if self.request.query_params:
    #         print(dict(self.request.query_params))
    #         queryset = queryset.filter(**dict(self.request.query_params))
    #         return queryset
    #     return User.objects.all().order_by('-date_joined')


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all().order_by('name')
    serializer_class = serializers.DeviceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDeviceViewSet(viewsets.ModelViewSet):
    queryset = UserDevice.objects.all().order_by('device')
    serializer_class = serializers.UserDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]


class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = serializers.HomeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
