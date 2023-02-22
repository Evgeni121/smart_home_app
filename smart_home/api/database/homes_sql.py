import sqlite3
from sqlite3 import Error

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def create_table_homes_sql():
    name = "create_homes"
    sql = """
        CREATE TABLE IF NOT EXISTS homes (
        home_id INTEGER PRIMARY KEY AUTOINCREMENT,
        home_name TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        UNIQUE (home_id, user_id)
        );
    """
    execute_write(sql, name)


def get_home_database_sql(**kwargs):
    name = "get_home"
    if "home_id" in kwargs.keys():
        sql = f"""SELECT * FROM homes WHERE home_id = '{kwargs["home_id"]}'"""
    elif "user_id" in kwargs.keys():
        sql = f"""SELECT * FROM homes WHERE user_id = '{kwargs["user_id"]}'"""
    else:
        sql = f"SELECT * FROM homes"
    return execute_read(sql, name)


def get_wholly_home_database_sql(home_id):
    name = "get_wholly_home"
    sql = f"""
    SELECT * 
    FROM 
        rooms
        LEFT JOIN room_devices USING (room_id)
        LEFT JOIN devices USING (device_id)
    WHERE home_id = '{home_id}'"""
    return execute_read(sql, name)


def insert_home_database_sql(**kwargs):
    name = "insert_home_database"
    sql = (f"""
    INSERT INTO homes (home_name, user_id)
    VALUES (
     '{kwargs["home_name"]}',
     '{kwargs["user_id"]}'
     )
""")
    return execute_write(sql, name)


def update_home_database_sql(**kwargs):
    name = "update_home_database"
    sql = (f"""
    UPDATE homes 
    SET 
    home_name = '{kwargs["home_name"]}'
    WHERE 
    home_id = '{kwargs["home_id"]}'
""")
    return execute_write(sql, name)


def delete_home_database_sql(home_id):
    name = "delete_home_database"
    sql = (f"""
    DELETE FROM homes 
    WHERE 
    home_id = '{home_id}'
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


create_table_homes_sql()
if not get_home_database_sql():
    insert_home_database_sql(home_name="House", user_id=1)
    insert_home_database_sql(home_name="Apartment", user_id=1)
    insert_home_database_sql(home_name="Сottage", user_id=2)

