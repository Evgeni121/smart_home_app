import sqlite3
from sqlite3 import Error

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def create_table_rooms_sql():
    name = "create_rooms"
    sql = """
        CREATE TABLE IF NOT EXISTS rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT NOT NULL,
        home_id INTEGER NOT NULL,
        FOREIGN KEY (home_id) REFERENCES homes(home_id),
        UNIQUE (room_id, home_id)
        );
    """
    execute_write(sql, name)


def get_room_database_sql(**kwargs):
    name = "get_room"
    if "room_id" in kwargs.keys():
        sql = f"""SELECT * FROM rooms WHERE room_id = '{kwargs["room_id"]}'"""
    elif "home_id" in kwargs.keys():
        sql = f"""SELECT * FROM rooms WHERE home_id = '{kwargs["home_id"]}'"""
    else:
        sql = f"SELECT * FROM rooms"
    return execute_read(sql, name)


def insert_room_database_sql(**kwargs):
    name = "insert_room_database"
    sql = (f"""
    INSERT INTO rooms (room_name, home_id)
    VALUES (
     '{kwargs["room_name"]}',
     '{kwargs["home_id"]}'
     )
""")
    return execute_write(sql, name)


def update_room_database_sql(**kwargs):
    name = "update_room_database"
    sql = (f"""
    UPDATE rooms 
    SET 
    room_name = '{kwargs["room_name"]}'
    WHERE 
    room_id = '{kwargs["room_id"]}'
""")
    return execute_write(sql, name)


def delete_room_database_sql(room_id):
    name = "delete_room_database"
    sql = (f"""
    DELETE FROM rooms 
    WHERE 
    room_id = '{room_id}'
""")
    return execute_write(sql, name)


def execute_write(sql, name):
    try:
        cursor.execute(sql)
        connection.commit()
        print(f"{name} completed successfully")
        return True
    except Error as e:
        print(f"The error ->{e}<- occurred during {name}")
        return False


def execute_read(sql, name):
    try:
        cursor.execute(sql)
        rooms = cursor.fetchall()
        return rooms
    except Error as e:
        print(f"The error ->{e}<- occurred during {name}")
        return False


create_table_rooms_sql()
if not get_room_database_sql():
    insert_room_database_sql(room_name="Room_1", home_id=1)
    insert_room_database_sql(room_name="Room_2", home_id=1)
    insert_room_database_sql(room_name="Room_3", home_id=1)
    insert_room_database_sql(room_name="Room", home_id=2)
