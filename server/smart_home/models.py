from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    class Type(models.IntegerChoices):
        CONTROLLER = 1
        SENSOR = 2
        EXECUTIVE_OBJECT = 3

    class Category(models.IntegerChoices):
        HOME_SECURITY = 1
        FIRE_SAFETY = 2
        WATER_SUPPLY = 3
        ELECTRICITY_SUPPLY = 4
        VIDEO_SUPERVISION = 5
        CLIMATIZATION = 6
        LIGHTING = 7
        METERS = 8
        ALERT = 9
        POWER = 10

    class Interface(models.IntegerChoices):
        WI_FI = 1
        ETHERNET = 2
        RS_485 = 3

    TYPE = {
        Type.CONTROLLER: "Controller",
        Type.SENSOR: "Sensor",
        Type.EXECUTIVE_OBJECT: "Object"
    }

    CATEGORY = {
        Category.HOME_SECURITY: "Home Security",
        Category.FIRE_SAFETY: "Fire Safety",
        Category.WATER_SUPPLY: "Water Supply",
        Category.ELECTRICITY_SUPPLY: "Electricity Supply",
        Category.VIDEO_SUPERVISION: "Video Supervision",
        Category.CLIMATIZATION: "Climatization",
        Category.LIGHTING: "Lighting",
        Category.METERS: "Meters",
        Category.ALERT: "Alert",
        Category.POWER: "Power"
    }

    INTERFACE = {
        Interface.WI_FI: "Wi-Fi",
        Interface.ETHERNET: "Ethernet",
        Interface.RS_485: "RS-485"
    }

    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    device_category = models.IntegerField(
        choices=Category.choices,
        default=Category.HOME_SECURITY,
    )
    device_type = models.IntegerField(
        choices=Type.choices,
        default=Type.CONTROLLER,
    )
    interface = models.IntegerField(
        choices=Interface.choices,
        default=Interface.WI_FI,
    )
    ip = models.CharField(max_length=50,  default="", blank=True)

    class Meta:
        unique_together = ('name', 'model',)
        ordering = ['name']

    def __str__(self):
        return f"Device name: {self.name}, Device model: {self.model}"


class Home(models.Model):
    name = models.CharField(max_length=50, default="My home")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')
        ordering = ['name']

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50, default="My room")
    home = models.ForeignKey(Home, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'home')
        ordering = ['name']

    def __str__(self):
        return self.name


class HomeDevice(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    note = models.CharField(max_length=50, default="Usage...")
    home = models.ForeignKey(Home, default=None, on_delete=models.NOT_PROVIDED)

    class Meta:
        unique_together = ('device', 'note')
        ordering = ['device']


class RoomDevice(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    note = models.CharField(max_length=50, default="Usage...")
    room = models.ForeignKey(Room, default=None, on_delete=models.NOT_PROVIDED)

    class Meta:
        unique_together = ('device', 'note')
        ordering = ['device']


# device1 = Device(name="123", model="R-12", device_category=3, device_type=1)
# device2 = Device(name="234", model="R-13", device_category=3, device_type=1)
# device3 = Device(name="345", model="CD-122", device_category=3, device_type=1)
# device4 = Device(name="456", model="CV-122", device_category=3, device_type=1)
# device5 = Device(name="567", model="MD1232", device_category=3, device_type=1)
# device6 = Device(name="678", model="RW-1432", device_category=3, device_type=1)
# device7 = Device(name="789", model="RQ-1642", device_category=3, device_type=1)
# device8 = Device(name="890", model="RB-1232", device_category=3, device_type=1)
# device9 = Device(name="901", model="RD-1212", device_category=3, device_type=1)
# device10 = Device(name="012", model="GR-142", device_category=3, device_type=1)
#
# device1.save()
# device2.save()
# device3.save()
# device4.save()
# device5.save()
# device6.save()
# device7.save()
# device8.save()
# device9.save()
# device10.save()
