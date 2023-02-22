from smart_home.api.classes.user_cls import User
from smart_home.api.classes.home_cls import Home

from smart_home.api.database.users_sql import get_user_database_sql, get_user_homes_database_sql, \
    insert_user_database_sql, update_user_database_sql, delete_user_database_sql


def get_user(**kwargs):
    users = []
    for user in get_user_database_sql(**kwargs):
        users.append(User(user_id=user[0],
                          nickname=user[1],
                          email=user[2],
                          password=user[3],
                          remember_password=user[4],
                          status=user[5],
                          user_home_active_id=user[6]))
    return users


def get_user_homes(**kwargs):
    users_from_db = get_user_homes_database_sql(**kwargs)
    user = None
    if users_from_db:
        user_from_db = users_from_db[0]
        user = User(user_id=user_from_db[0],
                    nickname=user_from_db[1],
                    email=user_from_db[2],
                    password=user_from_db[3],
                    remember_password=user_from_db[4],
                    status=user_from_db[5],
                    user_home_active_id=user_from_db[6])
        for home in users_from_db:
            if home[8] and home[7]:
                user.homes[home[8]] = Home(user=user,
                                           name=home[8],
                                           home_id=home[7])
    return user


def insert_user(user: User):
    return insert_user_database_sql(user_nickname=user.nickname,
                                    user_email=user.email,
                                    user_password=user.password,
                                    user_remember_password=user.remember_password,
                                    user_status=user.status,
                                    user_home_active_id=user.user_home_active_id)


def update_user(user: User):
    return update_user_database_sql(user_id=user.user_id,
                                    user_nickname=user.nickname,
                                    user_email=user.email,
                                    user_password=user.password,
                                    user_remember_password=user.remember_password,
                                    user_status=user.status,
                                    user_home_active_id=user.user_home_active_id)


def delete_user(user: User):
    return delete_user_database_sql(user_id=user.user_id)
