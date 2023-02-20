import sqlite3
from sqlite3 import Error

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def create_table_home_devices_sql():
    name = "create_home_devices"
    sql = """
        CREATE TABLE IF NOT EXISTS home_devices (
        home_device_id INTEGER PRIMARY KEY AUTOINCREMENT,
        home_id INTEGER NOT NULL,
        device_id INTEGER NOT NULL,
        FOREIGN KEY (home_id) REFERENCES homes(home_id),
        FOREIGN KEY (device_id) REFERENCES devices(device_id),
        UNIQUE (home_id, device_id)
        );
        """
    execute_write(sql, name)


def get_home_devices_database_sql(home_id):
    name = "get_home_devices"
    sql = f"""SELECT * FROM home_devices WHERE home_id = {home_id}"""
    return execute_read(sql, name)


def get_home_devices_name_database_sql(home_id):
    name = "get_home_device_name"
    sql = f"""SELECT home_device_id, home_id, device_id, device_name, device_model, device_category, device_type, 
    device_interface, device_ip
    FROM 
        home_devices 
        JOIN devices USING (device_id)
    WHERE home_devices.home_id = {home_id}"""
    return execute_read(sql, name)


def insert_home_device_database_sql(**kwargs):
    name = "insert_home_device"
    sql = (f"""INSERT INTO home_devices (home_id, device_id)
     VALUES (
     '{kwargs["home_id"]}',
     '{kwargs["device_id"]}'
     )
""")
    return execute_write(sql, name)


def update_home_device_database_sql(**kwargs):
    name = "update_home_device"
    sql = (f"""
            UPDATE home_devices 
            SET 
            device_id = '{kwargs["device_id"]}'
            WHERE 
            home_device_id = '{kwargs["home_device_id"]}'
            """)
    return execute_write(sql, name)


def delete_home_device_database_sql(home_device_id):
    name = "delete_home_device"
    sql = (f"""
            DELETE FROM home_devices 
            WHERE 
            home_device_id = '{home_device_id}'
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
        homes = cursor.fetchall()
        return homes
    except Error as e:
        print(f"The error ->{e}<- occurred during {name}")
        return False


create_table_home_devices_sql()
if not get_home_devices_database_sql(1):
    insert_home_device_database_sql(home_id=1, device_id=2)
    insert_home_device_database_sql(home_id=1, device_id=4)
    insert_home_device_database_sql(home_id=1, device_id=7)
    insert_home_device_database_sql(home_id=1, device_id=8)
    insert_home_device_database_sql(home_id=1, device_id=11)

if not get_home_devices_database_sql(2):
    insert_home_device_database_sql(home_id=2, device_id=2)
    insert_home_device_database_sql(home_id=2, device_id=5)
    insert_home_device_database_sql(home_id=2, device_id=13)
