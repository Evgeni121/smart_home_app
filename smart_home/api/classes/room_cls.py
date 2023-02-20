from smart_home.api.classes.home_cls import Home


class Room:
    def __init__(self, home: Home,
                 name: str = "My room",
                 room_id: int = None):
        self._room_id = room_id
        self._name = name
        self._home = home
        self._devices = {}

    def __str__(self):
        return self._name

    @property
    def home(self):
        return self._home

    @property
    def room_id(self):
        return self._room_id

    @room_id.setter
    def room_id(self, room_id):
        self._room_id = room_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def devices(self):
        return self._devices

    @devices.setter
    def devices(self, devices):
        self._devices = devices
