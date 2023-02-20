from smart_home.api.classes.home_cls import Home
from smart_home.api.classes.device_cls import HomeDevice

from smart_home.api.database.home_devices_sql import get_home_devices_database_sql, get_home_devices_name_database_sql, \
    update_home_device_database_sql, insert_home_device_database_sql, delete_home_device_database_sql


def get_home_devices(home: Home):
    for home_device in get_home_devices_name_database_sql(home.home_id):
        home_device = HomeDevice(home_device_id=home_device[0],
                                 home_id=home_device[1],
                                 device_id=home_device[2],
                                 device_name=home_device[3],
                                 device_model=home_device[4],
                                 device_category=home_device[5],
                                 device_type=home_device[6],
                                 device_interface=home_device[7],
                                 device_ip=home_device[8])
        home.devices[home_device] = home_device
    return home


def insert_home_device(device: HomeDevice):
    return insert_home_device_database_sql(home_id=device.home_id,
                                           device_id=device.device_id)


def update_home_device(device: HomeDevice):
    return update_home_device_database_sql(home_device_id=device.home_device_id,
                                           device_id=device.device_id)


def delete_home_device(device: HomeDevice):
    return delete_home_device_database_sql(home_device_id=device.home_device_id)
