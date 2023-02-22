from smart_home.api.classes.room_cls import Room
from smart_home.api.classes.device_cls import RoomDevice

from smart_home.api.database.room_devices_sql import get_room_devices_database_sql, get_room_devices_name_database_sql, \
    update_room_device_database_sql, insert_room_device_database_sql, delete_room_device_database_sql


def get_room_devices(room: Room):
    for room_device in get_room_devices_name_database_sql(room.room_id):
        room_device = RoomDevice(room_device_id=room_device[0],
                                 room_id=room_device[1],
                                 device_id=room_device[2],
                                 device_name=room_device[3],
                                 device_model=room_device[4],
                                 device_category=room_device[5],
                                 device_type=room_device[6],
                                 device_interface=room_device[7],
                                 device_ip=room_device[8])
        room.devices[room_device.room_device_id] = room_device
    return room


def insert_room_device(device: RoomDevice):
    return insert_room_device_database_sql(room_id=device.room_id,
                                           device_id=device.device_id)


def update_room_device(device: RoomDevice):
    return update_room_device_database_sql(room_device_id=device.room_device_id,
                                           device_id=device.device_id)


def delete_room_device(device: RoomDevice):
    return delete_room_device_database_sql(room_device_id=device.room_device_id)
