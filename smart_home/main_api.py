from smart_home.api.classes.home_cls import Home
from smart_home.api.home_api import get_homes, get_wholly_home, insert_home, update_home, delete_home
from smart_home.api.home_devices_api import get_home_devices, insert_home_device, update_home_device, \
    delete_home_device

from smart_home.api.classes.room_cls import Room
from smart_home.api.room_api import get_rooms, insert_room, update_room, delete_room
from smart_home.api.room_devices_api import get_room_devices, insert_room_device, update_room_device, \
    delete_room_device

from smart_home.api.classes.device_cls import Device
from smart_home.api.device_api import get_device, insert_device, update_device, delete_device

from smart_home.api.classes.user_cls import User
from smart_home.api.user_api import get_user, get_user_homes, insert_user, update_user, delete_user


def create_device(**kwargs):
    insert_device(**kwargs)
    return get_device(device_name=kwargs["name"], device_model=kwargs["model"])
