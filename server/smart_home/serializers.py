from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'password']


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Device
        fields = ['url', 'id', 'name', 'model', 'category', 'type', 'interface', 'ip']


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Home
        fields = ['url', 'id', 'name', 'user', 'devices']


class HomeDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HomeDevice
        fields = ['url', 'id', 'home', 'device', 'description']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Room
        fields = ['url', 'id', 'name', 'home', 'devices']


class RoomDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RoomDevice
        fields = ['url', 'id', 'room', 'device', 'description']
