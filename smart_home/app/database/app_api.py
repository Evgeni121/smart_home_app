from smart_home.app.database.database_creation import create_table, AppUser
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///database.db', echo=False)
create_table(engine)
metadata_obj = MetaData()

table = Table("app_users", metadata_obj, autoload_with=engine)


def add_user(user):
    stmt = insert(table).values(user_id=user.user_id,
                                email=user.email,
                                password=user.password,
                                username=user.username,
                                user_authorized=user.user_authorized,
                                user_remember_password=user.user_remember_password,
                                user_home=user.user_home
                                )
    conn = engine.connect()
    try:
        conn.execute(stmt)
    except IntegrityError:
        return False
    finally:
        conn.commit()
    return True


def get_user(**kwargs):
    if "user_remember_password" in kwargs.keys():
        stmt = select(AppUser).where(AppUser.user_remember_password == kwargs["user_remember_password"])
    elif "user_authorized" in kwargs.keys():
        stmt = select(AppUser).where(AppUser.user_authorized == kwargs["user_authorized"])
    elif "username" in kwargs.keys():
        stmt = select(AppUser).where(AppUser.username == kwargs["username"])
    elif "id" in kwargs.keys():
        stmt = select(AppUser).where(AppUser.user_id == kwargs["id"])
    else:
        stmt = select(AppUser)
    app_users = {}
    conn = engine.connect()
    try:
        for data in conn.execute(stmt):
            user = AppUser(user_id=data.user_id,
                           email=data.email,
                           password=data.password,
                           username=data.username,
                           user_authorized=data.user_authorized,
                           user_remember_password=data.user_remember_password,
                           user_home=data.user_home
                           )
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
        .values(username=kwargs["username"] if kwargs.get("username") is not None else user.username,
                email=kwargs["email"] if kwargs.get("email") is not None else user.email,
                password=kwargs["password"] if kwargs.get("password") is not None else user.password,
                user_authorized=kwargs["user_authorized"] if kwargs.get("user_authorized") is not None
                else user.user_authorized,
                user_remember_password=kwargs["user_remember_password"]
                if kwargs.get("user_remember_password") is not None else user.user_remember_password,
                user_home=kwargs["user_home"] if kwargs.get("user_home") is not None else user.user_home)
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
