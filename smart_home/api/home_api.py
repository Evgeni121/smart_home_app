from smart_home.api.classes.home_cls import Home
from smart_home.api.classes.user_cls import User
from smart_home.api.classes.room_cls import Room
from smart_home.api.classes.device_cls import RoomDevice

from smart_home.api.database.homes_sql import get_home_database_sql, get_wholly_home_database_sql, \
    update_home_database_sql, insert_home_database_sql, delete_home_database_sql


def get_homes(user: User):
    homes = []
    for home in get_home_database_sql(user_id=user.user_id):
        homes.append(Home(home_id=home[0],
                          name=home[1],
                          user=user))
    return homes


def get_wholly_home(home: Home):
    rooms_from_db = get_wholly_home_database_sql(home_id=home.home_id)
    rooms = {}
    devices = {}
    for room in rooms_from_db:
        rooms[room[1]] = Room(room_id=room[0],
                              name=room[1],
                              home=home)
    for device in rooms_from_db:
        rooms[device[1]].devices[device[3]] = RoomDevice(room_device_id=device[3],
                                                         room_id=device[0],
                                                         device_id=device[4],
                                                         device_name=device[5],
                                                         device_model=device[6],
                                                         device_category=device[7],
                                                         device_type=device[8],
                                                         device_interface=device[9],
                                                         device_ip=device[10])
    return rooms


def insert_home(home: Home):
    return insert_home_database_sql(home_name=home.name,
                                    user_id=home.user.user_id)


def update_home(home: Home):
    return update_home_database_sql(home_name=home.name,
                                    home_id=home.home_id)


def delete_home(home: Home):
    return delete_home_database_sql(home_id=home.home_id)
