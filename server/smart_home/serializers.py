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


class UserDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserDevice
        fields = ['url', 'id', 'device', 'note']


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Home
        fields = ['url', 'id', 'name', 'user', 'user_device']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Room
        fields = ['url', 'id', 'name', 'home', 'user_device']
