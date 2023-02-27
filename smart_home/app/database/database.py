from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class AppUser(Base):
    __tablename__ = 'app_users'
    app_user_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    password = Column(String)
    user_authorized = Column(Boolean)
    users_remember_password = Column(Boolean)

    def __init__(self, user_id, username, password, user_authorized=False, users_remember_password=False):
        self._user_id = user_id,
        self._username = username,
        self._password = password,
        self._user_authorized = user_authorized,
        self._users_remember_password = users_remember_password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self._user_id, self._username, self._password)


Base.metadata.create_all(engine)
users_table = AppUser.__table__

Session = sessionmaker(bind=engine)
session = Session()

user = AppUser(1, "qwerty", "12345678")
user1 = AppUser(2, "qwerty1", "12345678")
user2 = AppUser(3, "qwerty2", "123456789")
session.add(user)
session.add(user1)
session.add(user2)

session.commit()

print(user1.app_user_id)

for user in session.query(AppUser).order_by(AppUser.app_user_id):
    print(user.username)
