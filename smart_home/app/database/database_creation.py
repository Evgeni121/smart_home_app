from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AppUser(Base):
    __tablename__ = 'app_users'
    app_user_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    user_authorized = Column(Boolean)
    user_remember_password = Column(Boolean)
    user_home = Column(Integer)

    def __init__(self, user_id, email, password, username, user_authorized=False,
                 user_remember_password=False,
                 user_home=0):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.user_authorized = user_authorized
        self.user_remember_password = user_remember_password
        self.user_home = user_home

    def __repr__(self):
        return "User: ('%s','%s', '%s', '%s', '%s', '%s', '%s')" % (self.user_id, self.username, self.email,
                                                                    self.password,
                                                                    self.user_authorized, self.user_remember_password,
                                                                    self.user_home)


def create_table(engine):
    Base.metadata.create_all(engine)
