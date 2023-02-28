from smart_home.app.database.database_creation import create_table, AppUser
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///database.db', echo=False)
create_table(engine)
metadata_obj = MetaData()

table = Table("app_users", metadata_obj, autoload_with=engine)


def add_user(**kwargs):
    stmt = insert(table).values(**kwargs)
    conn = engine.connect()
    try:
        conn.execute(stmt)
    except IntegrityError:
        return False
    finally:
        conn.commit()
    return True


def get_user(**kwargs):
    if "users_remember_password" in kwargs.keys():
        stmt = select(AppUser).where(AppUser.users_remember_password == kwargs["users_remember_password"])
    elif "user_authorized" in kwargs.keys():
        stmt = select(AppUser).where(AppUser.user_authorized == kwargs["user_authorized"])
    elif "username" in kwargs.keys():
        stmt = select(AppUser).where(AppUser.username == kwargs["username"])
    else:
        stmt = select(AppUser)
    app_users = {}
    conn = engine.connect()
    try:
        for user in conn.execute(stmt):
            app_users[user.user_id] = user
    except:
        return False
    finally:
        conn.commit()
    return app_users


def update_user(user, **kwargs):
    stmt = (
        update(table)
        .where(table.c.user_id == user.user_id)
        .values(username=kwargs["username"] if kwargs.get("username") else user.username,
                password=kwargs["password"] if kwargs.get("password") else user.password,
                user_authorized=kwargs["user_authorized"] if kwargs.get("user_authorized") else user.user_authorized,
                users_remember_password=kwargs["users_remember_password"] if kwargs.get("users_remember_password")
                else user.users_remember_password,
                user_home_id=kwargs["user_home_id"] if kwargs.get("user_home_id") else user.user_home)
    )
    conn = engine.connect()
    try:
        conn.execute(stmt)
    except:
        return False
    finally:
        conn.commit()
    return True


def delete_user(user):
    stmt = delete(table).where(table.c.user_id == user.user_id)
    conn = engine.connect()
    try:
        conn.execute(stmt)
    except:
        return False
    finally:
        conn.commit()
    return True


# add_user(user_id=2, username="qwerty", password="12345678")
# a = get_user(username="qwerty2")
# update_user(a[2], username="qwerty1")
# delete_user(a[2])
