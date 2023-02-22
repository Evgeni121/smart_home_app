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


def insert_device(**kwargs):
    return insert_device_database_sql(device_name=kwargs["name"],
                                      device_model=kwargs["model"],
                                      device_category=kwargs["category"],
                                      device_type=kwargs["type"],
                                      device_interface=None,
                                      device_ip=None)


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
