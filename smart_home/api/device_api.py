from smart_home.api.classes.device_cls import Device

from smart_home.api.database.devices_sql import get_device_database_sql, insert_device_database_sql, \
    update_device_database_sql, delete_device_database_sql


def get_device(**kwargs):
    devices = []
    for device in get_device_database_sql(**kwargs):
        devices.append(Device(device_id=device[0],
                              device_name=device[1],
                              device_model=device[2],
                              device_category=device[3],
                              device_type=device[4],
                              device_interface=device[5],
                              device_ip=device[6]))
    return devices


def insert_device(device: Device):
    return insert_device_database_sql(device_name=device.name,
                                      device_model=device.model,
                                      device_category=device.category,
                                      device_type=device.type,
                                      device_interface=device.interface,
                                      device_ip=device.device_ip)


def update_device(device: Device):
    return update_device_database_sql(device_id=device.device_id,
                                      device_name=device.name,
                                      device_model=device.model,
                                      device_category=device.category,
                                      device_type=device.type,
                                      device_interface=device.interface,
                                      device_ip=device.device_ip)


def delete_device(device_id):
    return delete_device_database_sql(device_id=device_id)
