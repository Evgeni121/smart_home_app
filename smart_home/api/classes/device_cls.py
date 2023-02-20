import enum


class Device:
    class Type(enum.Enum):
        controller = 1
        sensor = 2
        object = 3

        def __str__(self):
            return self.name

    class Category(enum.Enum):
        home_security = 1
        fire_safety = 2
        water_supply = 3
        electricity_supply = 4
        video_supervision = 5
        climatization = 6
        lighting = 7
        meters = 8
        alert = 9
        power = 10

        def __str__(self):
            return self.name

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

    def __init__(self,
                 device_name: str,
                 device_model: str,
                 device_category: int,
                 device_type: int,
                 device_interface: str = None,
                 device_ip: str = None,
                 device_id: int = None):
        self._device_id = device_id
        self._name = device_name
        self._model = device_model
        self._interface = device_interface
        self._category = self.Category(device_category)
        self._type = self.Type(device_type)
        self._device_ip = device_ip

    def __str__(self):
        return f"\nDevice name: {self._name}"\
               f"\nDevice model: {self._model}"\
               f"\nDevice category: {self.CATEGORY[self._category.value]}"\
               f"\nDevice type: {self.TYPE[self._type.value]}"

    # def __iter__(self):
    #     return self
    #
    # def __next__(self):
    #     return self

    @property
    def device_id(self):
        return self._device_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def category(self):
        return self._category.value

    @category.setter
    def category(self, category):
        self._category = self.Category(category)

    @property
    def type(self):
        return self._type.value

    @type.setter
    def type(self, device_type):
        self._type = self.Type(device_type)

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, interface):
        self._interface = interface

    @property
    def device_ip(self):
        return self._device_ip

    @device_ip.setter
    def device_ip(self, _device_ip):
        self._type = _device_ip


class HomeDevice(Device):
    def __init__(self, home_device_id: int, home_id: int, **kwargs):
        super().__init__(**kwargs)
        self._home_device_id = home_device_id
        self._home_id = home_id

    @property
    def home_device_id(self):
        return self._home_device_id

    @property
    def home_id(self):
        return self._home_id


class RoomDevice(Device):
    def __init__(self, room_device_id: int, room_id: int, **kwargs):
        super().__init__(**kwargs)
        self._room_device_id = room_device_id
        self._room_id = room_id

    @property
    def room_device_id(self):
        return self._room_device_id

    @property
    def room_id(self):
        return self._room_id
