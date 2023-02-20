from smart_home.api.classes.room_cls import Room
from smart_home.api.classes.home_cls import Home

from smart_home.api.database.rooms_sql import get_room_database_sql, update_room_database_sql, \
    insert_room_database_sql, delete_room_database_sql


def get_rooms(home: Home):
    rooms = []
    for room in get_room_database_sql(home_id=home.home_id):
        rooms.append(Room(room_id=room[0],
                          name=room[1],
                          home=home))
    return rooms


def get_room_devices(home: Home):
    rooms = []
    for room in get_room_database_sql(home_id=home.home_id):
        rooms.append(Room(room_id=room[0],
                          name=room[1],
                          home=home))
    return rooms


def insert_room(room: Room):
    return insert_room_database_sql(room_name=room.name,
                                    home_id=room.home.home_id)


def update_room(room: Room):
    return update_room_database_sql(room_name=room.name,
                                    room_id=room.room_id)


def delete_room(room: Room):
    return delete_room_database_sql(room_id=room.room_id)
