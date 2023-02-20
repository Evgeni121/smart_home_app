import sqlite3
from sqlite3 import Error

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def create_table_room_devices_sql():
    name = "create_room_devices"
    sql = """
        CREATE TABLE IF NOT EXISTS room_devices (
        room_device_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        device_id INTEGER NOT NULL,
        FOREIGN KEY (room_id) REFERENCES rooms(room_id),
        FOREIGN KEY (device_id) REFERENCES devices(device_id),
        UNIQUE (room_id, device_id)
        );
        """
    execute_write(sql, name)


def get_room_devices_database_sql(room_id):
    name = "get_room_devices"
    sql = f"""SELECT * FROM room_devices WHERE room_id = {room_id}"""
    return execute_read(sql, name)


def get_room_devices_name_database_sql(room_id):
    name = "get_room_device_name"
    sql = f"""SELECT room_device_id, room_id, device_id, device_name, device_model, device_category, device_type, 
    device_interface, device_ip
    FROM 
        room_devices 
        JOIN devices USING (device_id)
    WHERE room_devices.room_id = {room_id}"""
    return execute_read(sql, name)


def insert_room_device_database_sql(**kwargs):
    name = "insert_room_device"
    sql = (f"""INSERT INTO room_devices (room_id, device_id)
     VALUES (
     '{kwargs["room_id"]}',
     '{kwargs["device_id"]}'
     )
""")
    return execute_write(sql, name)


def update_room_device_database_sql(**kwargs):
    name = "update_room_device"
    sql = (f"""
            UPDATE room_devices 
            SET 
            device_id = '{kwargs["device_id"]}'
            WHERE 
            room_device_id = '{kwargs["room_device_id"]}'
            """)
    return execute_write(sql, name)


def delete_room_device_database_sql(room_device_id):
    name = "delete_room_device"
    sql = (f"""
            DELETE FROM room_devices 
            WHERE 
            room_device_id = '{room_device_id}'
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


create_table_room_devices_sql()
if not get_room_devices_database_sql(1):
    insert_room_device_database_sql(room_id=1, device_id=2)
    insert_room_device_database_sql(room_id=1, device_id=4)
    insert_room_device_database_sql(room_id=1, device_id=7)
    insert_room_device_database_sql(room_id=1, device_id=8)
    insert_room_device_database_sql(room_id=1, device_id=11)

    insert_room_device_database_sql(room_id=2, device_id=2)
    insert_room_device_database_sql(room_id=2, device_id=5)
    insert_room_device_database_sql(room_id=2, device_id=13)

    insert_room_device_database_sql(room_id=3, device_id=2)
    insert_room_device_database_sql(room_id=3, device_id=5)
    insert_room_device_database_sql(room_id=3, device_id=13)
