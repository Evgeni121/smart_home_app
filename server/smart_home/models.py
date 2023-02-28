from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    class Type(models.IntegerChoices):
        controller = 1
        sensor = 2
        object = 3

    class Category(models.IntegerChoices):
        Home_security = 1
        Fire_safety = 2
        Water_supply = 3
        Electricity_supply = 4
        Video_supervision = 5
        Climatization = 6
        Lighting = 7
        Meters = 8
        Alert = 9
        Power = 10

    class Interface(models.IntegerChoices):
        Wi_Fi = 1
        Ethernet = 2
        RS_485 = 3

    TYPE = {
        1: "Controller",
        2: "Sensor",
        3: "Object"
    }

    CATEGORY = {
        1: "Home Security",
        2: "Fire Safety",
        3: "Water Supply",
        4: "Electricity Supply",
        5: "Video Supervision",
        6: "Climatization",
        7: "Lighting",
        8: "Meters",
        9: "Alert",
        10: "Power"
    }

    INTERFACE = {
        1: "Wi-Fi",
        2: "Ethernet",
        3: "RS-485"
    }

    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    category = models.IntegerField(
        choices=Category.choices,
        default=Category.Home_security,
    )
    type = models.IntegerField(
        choices=Type.choices,
        default=Type.controller,
    )
    interface = models.IntegerField(
        choices=Interface.choices,
        default=Interface.Wi_Fi,
    )
    ip = models.CharField(max_length=50,  default="", blank=True)

    class Meta:
        unique_together = ('name', 'model',)
        ordering = ['name']

    def __str__(self):
        return f"Device name: {self.name}, Device model: {self.model}"


class UserDevice(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    note = models.CharField(max_length=50, default="Usage...")

    class Meta:
        unique_together = ('note', 'device')
        ordering = ['device']


class Home(models.Model):
    name = models.CharField(max_length=50, default="My home")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_device = models.ForeignKey(UserDevice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user', 'user_device')
        ordering = ['name']

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50, default="My room")
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    user_device = models.ForeignKey(UserDevice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'home', 'user_device')
        ordering = ['name']

    def __str__(self):
        return self.name


# device1 = Device(name="123", model="R-12", category=3, type=1)
# device2 = Device(name="234", model="R-13", category=3, type=1)
# device3 = Device(name="345", model="CD-122", category=3, type=1)
# device4 = Device(name="456", model="CV-122", category=3, type=1)
# device5 = Device(name="567", model="MD1232", category=3, type=1)
# device6 = Device(name="678", model="RW-1432", category=3, type=1)
# device7 = Device(name="789", model="RQ-1642", category=3, type=1)
# device8 = Device(name="890", model="RB-1232", category=3, type=1)
# device9 = Device(name="901", model="RD-1212", category=3, type=1)
# device10 = Device(name="012", model="GR-142", category=3, type=1)
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
