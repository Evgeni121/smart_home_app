from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem, \
    OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

from smart_home.app.authorization_screen import AuthorizationScreen, DialogList, MailLine, kv_authorization
from smart_home.app.main_screen import MainScreen, DeviceAdd, RightRaisedButton, \
    LeftRaiseButton, DeviceSettings, kv_bottom_navigation, RoomAdd, RoomChoice, RoomDeviceSettings, \
    DeviceProperties, LineWithSwitch

from smart_home.app.database import app_api

Builder.load_string(kv_authorization + kv_bottom_navigation)
screen_manager = ScreenManager()


class SmartHome(MDApp):
    TYPE = {
        1: "Controller",
        2: "Sensor",
        3: "Executive object"
    }

    CATEGORY = {
        1: "Home Security",
        2: "Fire Safety",
        3: "Water Supply",
        4: "Electricity Supply",
        5: "Video Supervision",
        6: "Climatization",
        7: "Lighting",
        8: "Meters",
        9: "Alert",
        10: "Power"
    }

    def __init__(self, server_api, driver, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.material_style = "M2"

        self.users = app_api.get_user()
        self.user_authorized = None
        for user in self.users.values():
            if user.user_authorized:
                self.user_authorized = user
                break

        self.devices = {}
        self.homes = {}
        self.home_devices = {}
        self.rooms = {}
        self.room_devices = {}
        self.server_api = server_api
        self.app_api = app_api
        self.driver = driver
        self.dialog = None
        self.dialog_2 = None
        self.menu = None
        self.auth = None

    def build(self):
        screen_1 = AuthorizationScreen(name='authorization_screen')
        screen_2 = MainScreen(name='main_screen')
        screen_manager.add_widget(screen_1)
        screen_manager.add_widget(screen_2)

        if self.user_authorized:
            screen_manager.current = 'main_screen'
        else:
            screen_manager.current = 'authorization_screen'
            self.field_filler()
        return screen_manager

    def on_start(self):
        try:
            self.devices = {device["id"]: device for device in self.server_api.get("devices")}
            self.set_list_devices()
        except TypeError:
            self.connection_error()

        if self.user_authorized:
            self.auth = (self.user_authorized.username, self.user_authorized.password)
            self.set_user_home()

    def set_list_devices(self, text="", search=False):
        screen_manager.screens[1].ids.bottom.ids.container.clear_widgets()

        def add_widget(current_device):
            screen_manager.screens[1].ids.bottom.ids.container.add_widget(
                TwoLineAvatarIconListItem(
                    RightRaisedButton(
                        MDIconButton(icon="minus",
                                     on_release=lambda x: self.delete_device_dialog(x))),
                    LeftRaiseButton(
                        MDIconButton(icon="cog",
                                     on_release=lambda x: self.settings_dialog(x))),
                    text=current_device["name"],
                    secondary_text=current_device["model"],
                    id=f"{current_device['id']}",
                    on_release=lambda x: self.add_room_device_dialog(x)))

        for device in self.devices.values():
            if search:
                if text in device["name"].lower() or text in device["name"]:
                    add_widget(device)
            else:
                add_widget(device)

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def log_in(self, email, password):
        remember_password = screen_manager.screens[0].ids.checkbox.ids.checkbox.active
        try:
            user = self.server_api.get("users", parameters={"email": email})
            if user:
                user = self.server_api.get("users", auth=(user[0]["username"], password), parameters={"email": email})
                if isinstance(user, list):
                    user = user[0]
                    if user["id"] in list(self.users.keys()):
                        self.user_authorized = self.users[user["id"]]
                        app_api.update_user(self.user_authorized, user_authorized=True)
                    else:
                        self.user_authorized = app_api.AppUser(user_id=user["id"],
                                                               email=user["email"],
                                                               username=user["username"],
                                                               password=password,
                                                               user_authorized=True,
                                                               user_remember_password=remember_password)
                        if remember_password:
                            self.users[self.user_authorized.user_id] = self.user_authorized
                        app_api.add_user(self.user_authorized)

                    self.auth = (email, password)
                    self.set_user_home()

                    screen_manager.transition.direction = 'left'
                    screen_manager.current = 'main_screen'
                    screen_manager.screens[0].ids.checkbox.ids.checkbox.active = False
                else:
                    screen_manager.screens[0].ids.password_field.ids.password_text_field.error = True
                    screen_manager.screens[0].ids.mail_field.ids.mail_text_field.error = False
            else:
                screen_manager.screens[0].ids.mail_field.ids.mail_text_field.error = True
                screen_manager.screens[0].ids.password_field.ids.password_text_field.error = False
        except TypeError:
            self.connection_error()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def set_user_home(self):
        self.homes = {}
        try:
            homes = self.server_api.get("homes", auth=(self.user_authorized.username, self.user_authorized.password),
                                        parameters={"user": self.user_authorized.user_id})
            if homes:
                self.homes = {home["id"]: home for home in homes}
                if self.user_authorized.user_home:
                    self.home_data_load(self.user_authorized.user_home)
                else:
                    self.home_list()
        except TypeError:
            self.connection_error()

    def home_list(self):
        home_list = DialogList()
        for home in self.homes.values():
            home_list.add_widget(
                OneLineAvatarIconListItem(
                    IconLeftWidget(icon="home"),
                    RightRaisedButton(
                        MDIconButton(icon="delete", on_release=lambda x: self.delete_home_dialog(x))),
                    id=f"{home['id']}",
                    text=home["name"],
                    on_release=lambda x: self.home_data_load(int(x.id))
                    if self.user_authorized.user_home != int(x.id)
                    else self.dialog_close()))

        self.dialog = MDDialog(
            title="My Homes",
            type="custom",
            width_offset=dp(20),
            content_cls=home_list,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="NEW",
                    theme_text_color="Hint",
                    on_release=lambda x: self.add_room_dialog("Home"))])
        self.dialog.open()

    def home_data_load(self, home_id):
        self.rooms = {}
        self.room_devices = {}
        screen_manager.screens[1].ids.bottom.ids.home_page.clear_widgets()

        if not self.user_authorized.user_home:
            try:
                self.app_api.update_user(self.user_authorized, user_home=home_id)
            except TypeError:
                self.connection_error()

        self.user_authorized.user_home = home_id
        screen_manager.screens[1].ids.home_name.title = self.homes[home_id]["name"]

        try:
            home_devices = self.server_api.get("home_devices", auth=self.auth, parameters={"home": home_id})
            self.home_devices = {home_device["id"]: home_device for home_device in home_devices}
            screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
                self.home_two_line_list_widget(self.homes[home_id], self.home_devices))
        except TypeError:
            self.connection_error()

        try:
            rooms = self.server_api.get("rooms", auth=self.auth, parameters={"home": home_id})
            for room in rooms:
                self.rooms[room["id"]] = room
                room_devices = self.server_api.get("room_devices",
                                                   auth=(self.user_authorized.username,
                                                         self.user_authorized.password),
                                                   parameters={"room": room["id"]})
                self.room_devices[room["id"]] = {room_device["id"]: room_device for room_device in room_devices}
                screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
                    self.room_two_line_list_widget(room, self.room_devices[room["id"]]))
        except TypeError:
            self.connection_error()

        if screen_manager.screens[1].ids.home_main.current == "Room devices":
            screen_manager.screens[1].ids.home_main.current = "Settings"

        if self.dialog:
            self.dialog_close()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def home_two_line_list_widget(self, home, home_devices):
        return TwoLineAvatarIconListItem(
            LeftRaiseButton(
                MDIconButton(icon="cog", on_release=lambda x: print("settings"))),
            text=home["name"],
            secondary_text=f"Devices: {len(home_devices)}",
            id=f"{home['id']}",
            on_release=lambda x: self.room_devices_list("home", home, home_devices))

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def room_two_line_list_widget(self, room, room_devices):
        return TwoLineAvatarIconListItem(
            RightRaisedButton(
                MDIconButton(icon="delete", on_release=lambda x: self.room_delete_dialog(x, room))),
            LeftRaiseButton(
                MDIconButton(icon="cog", on_release=lambda x: print("settings"))),
            text=room["name"],
            secondary_text=f"Devices: {len(room_devices)}",
            id=f"{room['id']}",
            on_release=lambda x: self.room_devices_list("room", room, room_devices))

    def room_devices_list(self, name, room, room_devices):
        screen_manager.screens[1].ids.room.ids.room_devices.clear_widgets()
        if room_devices:
            for device in room_devices.values():
                screen_manager.screens[1].ids.room.ids.room_devices.add_widget(
                    ThreeLineAvatarIconListItem(
                        RightRaisedButton(
                            MDIconButton(icon="minus", on_release=lambda x: self.delete_room_device_dialog(x, room))),
                        LeftRaiseButton(
                            MDIconButton(icon="cog", on_release=lambda x: self.room_device_settings_dialog(x,
                                                                                                           room,
                                                                                                           name))),
                        text=device["note"],
                        secondary_text=self.devices[device["device"]]["name"],
                        tertiary_text=self.devices[device["device"]]["model"],
                        id=f"{device['id']}",
                        on_release=lambda x: self.device_properties(int(x.id), room, name)))
        screen_manager.screens[1].ids.home_main.transition.direction = 'left'
        screen_manager.screens[1].ids.home_main.current = "Room devices"
        screen_manager.screens[1].ids.top_bar.title = f"{room['name']} devices"

    def room_device_settings_dialog(self, obj, room, name):
        primary_note = obj.parent.parent.parent.text
        device_settings = RoomDeviceSettings()
        device_settings.ids.note.text = primary_note

        self.dialog = MDDialog(
            title="Device:",
            type="custom",
            content_cls=device_settings,
            width_offset=dp(20),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="SAVE",
                    theme_text_color="Hint",
                    on_release=lambda x: self.room_device_setting(primary_note, device_settings,
                                                                  obj, room, name))])
        self.dialog.open()

    def room_device_setting(self, primary_note, device_settings, obj, room, name):
        device_note = device_settings.ids.note.text
        add_device = device_settings.ids.checkbox.ids.checkbox_add.active

        device_id = int(obj.parent.parent.parent.id)
        if primary_note != device_note or add_device:
            if name == "room":
                try:
                    self.server_api.put("room_devices", device_id, auth=self.auth,
                                        data={"note": device_note,
                                              "device": self.room_devices[room["id"]][device_id]["device"]})
                    obj.parent.parent.parent.text = device_note
                    self.room_devices[room["id"]][device_id]["note"] = device_note
                except TypeError:
                    self.connection_error()
            elif name == "home":
                try:
                    self.server_api.put("home_devices", device_id, auth=self.auth,
                                        data={"note": device_note, "device": self.home_devices[device_id]["device"]})
                    obj.parent.parent.parent.text = device_note
                    self.home_devices[device_id]["note"] = device_note
                except TypeError:
                    self.connection_error()

        self.add_device_to_home_page(add_device, obj)
        self.dialog_close()

    @staticmethod
    def add_device_to_home_page(state, widget):
        device_id = int(widget.parent.parent.parent.id)
        if state:
            print(f"Add to home page device {device_id}")
        else:
            print(f"Remove from home page device {device_id}")

    def device_properties(self, room_device_id, room, name):
        device_properties = []
        device_id = 0
        if name == "home":
            device_id = self.home_devices[room_device_id]["device"]
        elif name == "room":
            device_id = self.room_devices[room["id"]][room_device_id]["device"]
        try:
            device_properties = self.server_api.get("device_prop", auth=self.auth, parameters={"device": device_id})
        except TypeError:
            self.connection_error()

        content = DeviceProperties()
        for device_property in device_properties:
            content.ids.properties.add_widget(
                LineWithSwitch(
                    text=f"{device_property['name']}",
                    text_color=(0, 0, 0, 1),
                    font_style="Body1"))

        self.dialog = MDDialog(
            title="Device:",
            type="custom",
            content_cls=content,
            width_offset=dp(20),
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close)])
        self.dialog.open()

    def behavior(self, switch):
        print(switch.parent.parent.text)

    def delete_room_device_dialog(self, widget, room):
        note = widget.parent.parent.parent.text
        name = widget.parent.parent.parent.secondary_text
        model = widget.parent.parent.parent.tertiary_text
        self.dialog = MDDialog(
            title="Are you sure?",
            text=f"Do you want to delete device {note} {name} ({model})?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.delete_room_device(widget, room))])
        self.dialog.open()

    def delete_room_device(self, widget, room):
        device_id = int(widget.parent.parent.parent.id)
        if "rooms" in room["url"]:
            try:
                self.server_api.delete("room_devices", device_id, auth=self.auth)
            except TypeError:
                self.connection_error()
            self.room_devices[room['id']].pop(device_id)
        elif "homes" in room["url"]:
            try:
                self.server_api.delete("home_devices", device_id, auth=self.auth)
            except TypeError:
                self.connection_error()
            self.home_devices.pop(device_id)
        screen_manager.screens[1].ids.room.ids.room_devices.remove_widget(widget.parent.parent.parent)
        widgets = screen_manager.screens[1].ids.bottom.ids.home_page.children
        for line in widgets:
            if line.text == room["name"] and int(line.id) == room["id"]:
                if "homes" in room["url"]:
                    line.secondary_text = f"Devices: {len(self.home_devices)}"
                elif "rooms" in room["url"]:
                    line.secondary_text = f"Devices: {len(self.room_devices[room['id']])}"
        self.dialog_close()

    def room_delete_dialog(self, widget, room):
        self.dialog = MDDialog(
            title="Are you sure?",
            text=f"Do you want to delete room {room['name']}?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.delete_room(widget, room))])
        self.dialog.open()

    def delete_room(self, widget, room):
        try:
            self.server_api.delete("rooms", room["id"], auth=self.auth)
            screen_manager.screens[1].ids.bottom.ids.home_page.remove_widget(widget.parent.parent.parent)
            self.rooms.pop(room["id"])
            self.dialog_close()
        except TypeError:
            self.connection_error()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def delete_home_dialog(self, widget):
        self.dialog_2 = MDDialog(
            title="Are you sure?",
            text=f"Do you want to delete home {widget.parent.parent.parent.text}?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.delete_home(widget))])
        self.dialog_2.open()

    def delete_home(self, widget):
        home_id = int(widget.parent.parent.parent.id)
        try:
            self.server_api.delete("homes", home_id, auth=self.auth)
            self.homes.pop(home_id)
            if int(self.user_authorized.user_home) == home_id:
                self.app_api.update_user(self.user_authorized, user_home=0)
                self.user_authorized.user_home = 0
            screen_manager.screens[1].ids.home_name.title = f"Select a home!"
            screen_manager.screens[1].ids.bottom.ids.home_page.clear_widgets()
            self.dialog_close()
            self.home_list()
            self.dialog_2_close()
        except TypeError:
            self.connection_error()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def app_exit_dialog(self):
        self.dialog = MDDialog(
            title="Are you sure?",
            text="Do you want to go out?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.app_exit())])
        self.dialog.open()

    def app_exit(self):
        self.app_api.update_user(self.user_authorized, user_authorized=False)
        if not self.user_authorized.user_remember_password:
            self.app_api.delete_user(self.user_authorized)
        self.user_authorized = None
        self.homes = {}
        self.home_devices = {}
        self.rooms = {}
        self.room_devices = {}

        self.field_filler()
        screen_manager.transition.direction = 'right'
        screen_manager.current = 'authorization_screen'
        screen_manager.screens[1].ids.bottom.ids.home_page.clear_widgets()
        self.dialog_close()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def add_device_dialog(self):
        self.dialog = MDDialog(
            title="Device:",
            type="custom",
            content_cls=DeviceAdd(),
            width_offset=dp(20),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="ADD",
                    theme_text_color="Hint",
                    on_release=lambda x: self.add_device())])
        self.dialog.open()

    def add_device(self):
        name = self.dialog.content_cls.ids.name.text
        model = self.dialog.content_cls.ids.model.text
        device_category = self.dialog.content_cls.ids.category.id
        device_type = self.dialog.content_cls.ids.type.id
        if not device_category:
            self.dialog.content_cls.ids.category.error = True
        elif not device_type:
            self.dialog.content_cls.ids.type.error = True
        elif not name:
            self.dialog.content_cls.ids.name.error = True
        else:
            try:
                device = self.server_api.post("devices", auth=self.auth,
                                              data={"name": name,
                                                    "model": model,
                                                    "category": int(device_category),
                                                    "type": int(device_type)})
                if "non_field_errors" not in device.keys():
                    self.devices[device["id"]] = device
                    line = TwoLineAvatarIconListItem(
                        RightRaisedButton(
                            MDIconButton(icon="minus",
                                         on_release=lambda x: self.delete_device_dialog(x))),
                        LeftRaiseButton(
                            MDIconButton(icon="cog",
                                         on_release=lambda x: self.settings_dialog(x))),
                        text=name,
                        secondary_text=model,
                        id=f"{device['id']}")
                    screen_manager.screens[1].ids.bottom.ids.container.add_widget(line)
                    self.dialog_close()
                else:
                    self.snackbar("This device already exists!")
            except TypeError:
                self.connection_error()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def add_room_dialog(self, name):
        if self.dialog:
            self.dialog_close()
        self.dialog = MDDialog(
            title=f"New {name}:",
            type="custom",
            content_cls=RoomAdd(name),
            width_offset=dp(20),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="SAVE",
                    theme_text_color="Hint",
                    on_release=lambda x: self.add_room() if name == "Room" else self.add_home())])
        self.dialog.open()

    def add_home(self):
        name = self.dialog.content_cls.ids.name.text
        try:
            home = self.server_api.post("homes", auth=self.auth,
                                        data={"name": name,
                                              "user": self.user_authorized.user_id})
            if not name:
                self.dialog.content_cls.ids.name.error = True
            elif "non_field_errors" in home.keys():
                self.snackbar("This name already exists!")
            else:
                screen_manager.screens[1].ids.bottom.ids.home_page.clear_widgets()
                self.homes[home["id"]] = home
                screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
                    self.home_two_line_list_widget(home, []))
                screen_manager.screens[1].ids.home_name.title = self.homes[home["id"]]["name"]
                self.app_api.update_user(self.user_authorized, user_home=home["id"])
                self.user_authorized.user_home = home["id"]
                self.dialog_close()
        except TypeError:
            self.connection_error()

    def add_room(self):
        try:
            name = self.dialog.content_cls.ids.name.text
            room = self.server_api.post("rooms", auth=self.auth,
                                        data={"name": name,
                                              "home": self.user_authorized.user_home})
            if not name:
                self.dialog.content_cls.ids.name.error = True
            elif "non_field_errors" in room.keys():
                self.snackbar("This name already exists!")
            else:
                self.rooms[room["id"]] = room
                screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
                    self.room_two_line_list_widget(room, []))
                self.dialog_close()
        except TypeError:
            self.connection_error()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def add_room_device_dialog(self, widget):
        self.dialog = MDDialog(
            title=f"Select a room for device {widget.text} ({widget.secondary_text})",
            type="custom",
            content_cls=RoomChoice(),
            width_offset=dp(20),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="ADD",
                    theme_text_color="Hint",
                    on_release=lambda x: self.choice_room_save(widget))])
        self.dialog.open()

    def choice_room_list(self, obj):
        rooms = [room for room in self.rooms.values()]
        rooms.append(self.homes[self.user_authorized.user_home])
        menu_items = [
            {"id": f"{rooms[i]['id']}",
             "text": f"{rooms[i]['name']}",
             "viewclass": "OneLineListItem",
             "on_release": lambda x=rooms[i]: self.room_menu_callback(x, obj),
             } for i in range(len(rooms))]
        self.menu = MDDropdownMenu(
            caller=obj,
            items=menu_items,
            position="bottom",
            width_mult=4,
            max_height=dp(200))
        self.menu.open()

    def room_menu_callback(self, choice, obj):
        obj.text = choice["name"]
        obj.id = str(choice["id"])
        obj.obj = choice
        self.menu.dismiss()

    def choice_room_save(self, obj):
        note = self.dialog.content_cls.ids.note.text
        room = self.dialog.content_cls.ids.room.obj
        device_id = obj.id
        try:
            if room.get("home"):
                self.room_devices[room["id"]][device_id] = (self.server_api.post("room_devices",
                                                                                 auth=self.auth,
                                                                                 data={"note": note,
                                                                                       "device": device_id,
                                                                                       "room": room["id"]}))
                home_id = room["home"]
            elif room.get("user"):
                self.home_devices[device_id] = (self.server_api.post("home_devices",
                                                                     auth=self.auth,
                                                                     data={"note": note,
                                                                           "device": device_id,
                                                                           "home": room["id"]}))
                home_id = room["id"]
            else:
                home_id = self.user_authorized.user_home
            self.home_data_load(home_id)
            self.dialog_close()
            self.snackbar("Device added successfully")
        except TypeError:
            self.connection_error()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def delete_device_dialog(self, obj):
        name = obj.parent.parent.parent.text
        model = obj.parent.parent.parent.secondary_text
        self.dialog = MDDialog(
            title="Are you sure?",
            text=f"Do you want to delete device {name} ({model})?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.delete_device(obj))])
        self.dialog.open()

    def delete_device(self, obj):
        try:
            self.server_api.delete("devices", int(obj.parent.parent.parent.id), auth=self.auth)
            self.devices.pop(int(obj.parent.parent.parent.id))
            screen_manager.screens[1].ids.bottom.ids.container.remove_widget(obj.parent.parent.parent)
            self.dialog_close()
        except TypeError:
            self.connection_error()

    def settings_dialog(self, obj):
        primary_name = obj.parent.parent.parent.text
        primary_model = obj.parent.parent.parent.secondary_text

        device_settings = DeviceSettings()
        device_settings.ids.name.text = primary_name
        device_settings.ids.model.text = primary_model

        self.dialog = MDDialog(
            title="Device:",
            type="custom",
            content_cls=device_settings,
            width_offset=dp(20),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="SAVE",
                    theme_text_color="Hint",
                    on_release=lambda x: self.device_setting(primary_name, primary_model, device_settings, obj))])
        self.dialog.open()

    def device_setting(self, primary_device_name, primary_model, device_settings, obj):
        device_name = device_settings.ids.name.text
        device_model = device_settings.ids.model.text

        device_id = int(obj.parent.parent.parent.id)
        if primary_device_name != device_name or primary_model != device_model:
            try:
                self.server_api.put("devices", device_id, auth=self.auth,
                                    data={"name": device_name,
                                          "model": device_model})
                obj.parent.parent.parent.text = device_name
                obj.parent.parent.parent.secondary_text = device_model
                self.devices[device_id]["name"] = device_name
                self.devices[device_id]["model"] = device_model
            except TypeError:
                self.connection_error()
        self.dialog_close()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def mail_list(self):
        dialog = DialogList()
        if len(self.users) > 1:
            for user in self.users:
                dialog.add_widget(
                    MailLine(
                        id=f"{user}",
                        text=self.users[user].email,
                        icon=f"app/data/imgs/accounts/{self.users[user].email}.png",
                        on_release=lambda x: self.choice_mail(x.text, x.id)))
            self.dialog = MDDialog(
                title="Saved mails",
                type="custom",
                width_offset=dp(20),
                content_cls=dialog,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.dialog_close)])
            self.dialog.open()

    def choice_mail(self, text, user_id):
        screen_manager.screens[0].ids.mail_field.ids.mail_text_field.text = text
        screen_manager.screens[0].ids.password_field.ids.password_text_field.text = self.users[int(user_id)].password
        self.dialog_close()

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def open_list(self, obj):
        if obj.hint_text == "Type":
            object_dict = self.TYPE
        else:
            object_dict = self.CATEGORY
        menu_items = [
            {"id": f"{i}",
             "text": f"{object_dict[i]}",
             "viewclass": "OneLineListItem",
             "on_release": lambda x=f"{object_dict[i]}": self.menu_callback(x, obj, i),
             } for i in range(1, len(object_dict) + 1)]
        self.menu = MDDropdownMenu(
            caller=obj,
            items=menu_items,
            position="bottom",
            width_mult=4,
            max_height=dp(200))
        self.menu.open()

    def menu_callback(self, text_item, obj, i):
        obj.text = text_item
        obj.id = str(i)
        self.menu.dismiss()

    def field_filler(self):
        if len(self.users) == 1:
            screen_manager.screens[0].ids.mail_field.ids.mail_text_field.text = \
                self.users[list(self.users.keys())[0]].email
            screen_manager.screens[0].ids.password_field.ids.password_text_field.text = \
                self.users[list(self.users.keys())[0]].password
        else:
            screen_manager.screens[0].ids.mail_field.ids.mail_text_field.text = ""
            screen_manager.screens[0].ids.password_field.ids.password_text_field.text = ""

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def dialog_2_close(self, *args):
        self.dialog_2.dismiss(force=True)

    def connection_error(self):
        self.dialog = MDDialog(
            title="Connection Error",
            text="Check Internet Connection!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog_close())])
        self.dialog.open()

    @staticmethod
    def change_screen(screen_name):
        screen_manager.screens[1].ids.home_main.transition.direction = 'right'
        screen_manager.screens[1].ids.home_main.current = screen_name

    @staticmethod
    def forgot_password():
        print(f"Forgot Password")

    @staticmethod
    def sign_up():
        print(f"Sign Up")

    @staticmethod
    def snackbar(text):
        app_snackbar = Snackbar(
            text=f"[color='black']{text}[/color]",
            snackbar_x="10dp",
            snackbar_y="10dp",
            duration=1,
            bg_color=(1, 1, 1, 1))
        app_snackbar.size_hint_x = (Window.width - (app_snackbar.snackbar_x * 2)) / Window.width
        app_snackbar.buttons = [
            MDFlatButton(
                text="OK",
                text_color=(1, 1, 1, 1),
                on_release=app_snackbar.dismiss)]
        app_snackbar.open()
