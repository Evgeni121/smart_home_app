class User:
    # password = PasswordValidator()

    def __init__(self,
                 email: str,
                 password: str,
                 remember_password: bool = False,
                 status: bool = False,
                 user_id: int = None,
                 nickname: str = "User",
                 user_home_active_id: int = None):
        self._user_id = user_id
        self._nickname = nickname
        self._email = email
        self._password = password
        self._remember_password = remember_password
        self._status = status
        self._user_home_active_id = user_home_active_id
        self._homes = {}

    def __str__(self):
        return f"{self._nickname} {self._email}"

    @property
    def user_id(self):
        return self._user_id

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, nickname):
        self._nickname = nickname

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def remember_password(self):
        return self._remember_password

    @remember_password.setter
    def remember_password(self, remember_password):
        self._remember_password = remember_password

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def user_home_active_id(self):
        return self._user_home_active_id

    @user_home_active_id.setter
    def user_home_active_id(self, user_home_active_id):
        self._user_home_active_id = user_home_active_id

    @property
    def homes(self):
        return self._homes

    @homes.setter
    def homes(self, homes):
        self._homes = homes


class PasswordValidator:
    def __set_name__(self, obj, name):
        setattr(obj, f"__validated_{name}", "")
        self.__name = name

    def __set__(self, obj, value):
        if len(value) < 8:
            raise RuntimeError("Password is too short")
        setattr(obj, f"__validated_{self.__name}", value.strip())

    def __get__(self, obj, objtype=None):
        return getattr(obj, f"__validated_{self.__name}")
