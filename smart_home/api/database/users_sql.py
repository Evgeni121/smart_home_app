import sqlite3
from sqlite3 import Error

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def create_table_users_sql():
    name = "create_users"
    sql = """
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_nickname TEXT,
        user_email TEXT NOT NULL UNIQUE,
        user_password TEXT NOT NULL,
        user_remember_password INTEGER(1),
        user_status INTEGER(1),
        user_home_active_id INTEGER
        )
    """
    execute_write(sql, name)


def get_user_database_sql(**kwargs):
    name = "get_user_database"
    if "user_id" in kwargs.keys():
        sql = f"""SELECT * FROM users WHERE user_id = '{kwargs["user_id"]}'"""
    elif "user_email" in kwargs.keys():
        sql = f"""SELECT * FROM users WHERE user_email = '{kwargs["user_email"]}'"""
    elif "user_status" in kwargs.keys():
        sql = f"""SELECT * FROM users WHERE user_status = {kwargs["user_status"]}"""
    elif "users_remember_password" in kwargs.keys():
        sql = f"""SELECT * FROM users WHERE user_remember_password = {kwargs["users_remember_password"]}"""
    else:
        sql = f"SELECT * FROM users"
    return execute_read(sql, name)


def get_user_homes_database_sql(**kwargs):
    name = "get_user_homes_database"
    sql = None
    if "user_status" in kwargs.keys():
        sql = f"""SELECT *
        FROM 
            users
            LEFT JOIN homes USING (user_id)
        WHERE user_status = '{kwargs["user_status"]}'"""
    elif "user_email" in kwargs.keys():
        sql = f"""SELECT *
        FROM 
            users
            LEFT JOIN homes USING (user_id)
        WHERE user_email = '{kwargs["user_email"]}'"""
    return execute_read(sql, name)


def insert_user_database_sql(**kwargs):
    name = "insert_user_database"
    sql = (f"""
    INSERT INTO users (user_nickname, user_email, user_password, user_remember_password, user_status, 
    user_home_active_id)
    VALUES (
     '{kwargs["user_nickname"]}',
     '{kwargs["user_email"]}',
     '{kwargs["user_password"]}',
     '{kwargs["user_remember_password"]}',
     '{kwargs["user_status"]}',
     '{kwargs["user_home_active_id"]}'
     )
""")
    return execute_write(sql, name)


def update_user_database_sql(**kwargs):
    name = "update_user_database"
    sql = (f"""
    UPDATE users 
    SET 
    user_nickname = '{kwargs["user_nickname"]}',
    user_email = '{kwargs["user_email"]}',
    user_password = '{kwargs["user_password"]}',
    user_remember_password = '{kwargs["user_remember_password"]}',
    user_status = '{kwargs["user_status"]}',
    user_home_active_id = '{kwargs["user_home_active_id"]}'
    WHERE 
    user_id = '{kwargs["user_id"]}'
""")
    return execute_write(sql, name)


def delete_user_database_sql(user_id):
    name = "delete_user_database"
    sql = (f"""
    DELETE FROM users 
    WHERE 
    user_id = '{user_id}'
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


create_table_users_sql()
if not get_user_database_sql():
    insert_user_database_sql(user_nickname="", user_email="Smart@mail.ru", user_password="admin",
                             user_remember_password=1, user_status=1, user_home_active_id=1)
    insert_user_database_sql(user_nickname="", user_email="Home@mail.ru", user_password="admin",
                             user_remember_password=0, user_status=0, user_home_active_id=0)
    insert_user_database_sql(user_nickname="", user_email="1234", user_password="1234",
                             user_remember_password=0, user_status=0, user_home_active_id=0)
