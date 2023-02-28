from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AppUser(Base):
    __tablename__ = 'app_users'
    app_user_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    password = Column(String)
    user_authorized = Column(Boolean)
    users_remember_password = Column(Boolean)
    user_home_id = Column(Integer)

    def __init__(self, user_id, username, password, user_authorized=False, users_remember_password=False, user_home_id=0):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.user_authorized = user_authorized
        self.users_remember_password = users_remember_password
        self.user_home_id = user_home_id

    def __repr__(self):
        return "User: ('%s','%s', '%s', '%s', '%s', '%s')" % (self.user_id, self.username, self.password,
                                                              self.user_authorized, self.users_remember_password,
                                                              self.user_home_id)


def create_table(engine):
    Base.metadata.create_all(engine)
