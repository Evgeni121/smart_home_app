from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Device
        fields = ['url', 'id', 'name', 'model', 'device_category', 'device_type', 'interface', 'ip']


class DevicePropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DeviceProperties
        fields = ['url', 'id', 'device', "name", 'input', 'output', 'min_value', 'max_value']


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Home
        fields = ['url', 'id', 'name', 'user']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Room
        fields = ['url', 'id', 'name', 'home']


class HomeDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HomeDevice
        fields = ['url', 'id', 'device', 'note', 'home']


class RoomDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RoomDevice
        fields = ['url', 'id', 'device', 'note', 'room']
