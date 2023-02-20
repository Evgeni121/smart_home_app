from smart_home.api.classes.user_cls import User


class Home:
    def __init__(self, user: User,
                 name: str = "My Home",
                 home_id: int = None):
        self._home_id = home_id
        self._name = name
        self._user = user
        self._rooms = {}
        self._devices = {}

    def __str__(self):
        return self._name

    @property
    def user(self):
        return self._user

    @property
    def home_id(self):
        return self._home_id

    @home_id.setter
    def home_id(self, home_id):
        self._home_id = home_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def rooms(self):
        return self._rooms

    @rooms.setter
    def rooms(self, rooms):
        self._rooms = rooms

    @property
    def devices(self):
        return self._devices

    @devices.setter
    def devices(self, devices):
        self._devices = devices
