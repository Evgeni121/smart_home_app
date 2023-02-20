import sqlite3
from sqlite3 import Error

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def create_table_devices_sql():
    name = "create_devices"
    sql = """
        CREATE TABLE IF NOT EXISTS devices (
        device_id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_name TEXT NOT NULL,
        device_model TEXT NOT NULL,
        device_category INTEGER NOT NULL, 
        device_type INTEGER NOT NULL, 
        device_interface TEXT, 
        device_ip TEXT,
        UNIQUE (device_name, device_model)
        );
    """
    execute_write(sql, name)


def get_device_database_sql(**kwargs):
    name = "get_device"
    if "device_id" in kwargs.keys():
        sql = f"""SELECT * FROM devices WHERE device_id = '{kwargs["device_id"]}'"""
    elif "device_model" in kwargs.keys() and "device_name" in kwargs.keys():
        sql = f"""SELECT * FROM devices 
        WHERE device_model = '{kwargs["device_model"]}' AND device_name = '{kwargs["device_name"]}'"""
    elif "device_name" in kwargs.keys():
        sql = f"""SELECT * FROM devices WHERE device_name = '{kwargs["device_name"]}'"""
    elif "device_model" in kwargs.keys():
        sql = f"""SELECT * FROM devices WHERE device_model = '{kwargs["device_model"]}'"""
    else:
        sql = f"SELECT * FROM devices"
    return execute_read(sql, name)


def insert_device_database_sql(**kwargs):
    name = "insert_device"
    sql = (f"""
    INSERT INTO devices (device_name, device_model, device_category, device_type, device_interface, device_ip)
     VALUES (
     '{kwargs["device_name"]}',
     '{kwargs["device_model"]}',
     '{kwargs["device_category"]}',
     '{kwargs["device_type"]}',
     '{kwargs["device_interface"]}',
     '{kwargs["device_ip"]}'
     )
    """)
    return execute_write(sql, name)


def update_device_database_sql(**kwargs):
    name = "update_device"
    sql = (f"""
            UPDATE devices 
            SET 
            device_name = '{kwargs["device_name"]}',
            device_model = '{kwargs["device_model"]}',
            device_category = '{kwargs["device_category"]}',
            device_type = '{kwargs["device_type"]}',
            device_interface = '{kwargs["device_interface"]}',
            device_ip = '{kwargs["device_ip"]}'
            WHERE 
            device_id = '{kwargs["device_id"]}'
            """)
    return execute_write(sql, name)


def delete_device_database_sql(device_id):
    name = "delete_device"
    sql = (f"""
            DELETE FROM devices 
            WHERE 
            device_id = '{device_id}'
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
        users = cursor.fetchall()
        return users
    except Error as e:
        print(f"The error ->{e}<- occurred during {name}")
        return False


create_table_devices_sql()
if not get_device_database_sql():
    insert_device_database_sql(device_name="Door lock", device_model="RK-101", device_category=2,
                               device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Door lock", device_model="RK-103", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Security alarm", device_model="QWERTY", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Security alarm", device_model="JAZ", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Security alarm", device_model="HOME SEC-23", device_category=1,
                               device_type=1, device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Home security", device_model="ANUPOSHEL", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Home security", device_model="PYATKI", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Home security", device_model="RK-101", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Electricity meter", device_model="Smart Electro", device_category=1,
                               device_type=1, device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Electricity meter", device_model="Electro chainik", device_category=1,
                               device_type=1, device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Switch", device_model="REK-10s1", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Switch", device_model="RwK-10s1", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
    insert_device_database_sql(device_name="Switch", device_model="RvdK-10s1", device_category=1, device_type=1,
                               device_interface=None, device_ip=None)
