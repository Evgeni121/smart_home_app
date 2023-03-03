from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem, \
    OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

from smart_home.app.authorization_screen import AuthorizationScreen, DialogList, MailLine, kv_authorization
from smart_home.app.main_screen import MainScreen, DeviceAdd, RightRaisedButton, \
    LeftRaiseButton, DeviceSettings, kv_bottom_navigation, RoomAdd

from smart_home.app.database import app_api

Builder.load_string(kv_authorization + kv_bottom_navigation)
screen_manager = ScreenManager()


class SmartHome(MDApp):
    TYPE = {
        1: "Controller",
        2: "Sensor",
        3: "Object"
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

    def __init__(self, server_api, **kwargs):
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

        self.devices = {device["id"]: device for device in server_api.get("devices")}
        self.homes = {}
        self.home_devices = []
        self.rooms = {}
        self.room_devices = {}
        self.server_api = server_api
        self.app_api = app_api
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
        self.set_list_devices()

        if self.user_authorized:
            self.auth = (self.user_authorized.username, self.user_authorized.password)
            self.set_user_home()

    def set_list_devices(self, text="", search=False):
        screen_manager.screens[1].ids.bottom.ids.container.clear_widgets()

        def add_widget(available_device):
            screen_manager.screens[1].ids.bottom.ids.container.add_widget(
                TwoLineAvatarIconListItem(
                    RightRaisedButton(
                        MDIconButton(icon="minus",
                                     on_release=lambda x: self.delete_device_dialog(x))),
                    LeftRaiseButton(
                        MDIconButton(icon="cog",
                                     on_release=lambda x: self.settings_dialog(x))),
                    text=available_device["name"],
                    secondary_text=available_device["model"],
                    id=f"{available_device['id']}"))

        for device in self.devices.values():
            if search:
                if text in device["name"].lower() or text in device["name"]:
                    add_widget(device)
            else:
                add_widget(device)

    def log_in(self, email, password):
        remember_password = screen_manager.screens[0].ids.checkbox.ids.checkbox.active
        user = self.server_api.get("users", parameters={"email": email})
        if user:
            user = self.server_api.get("users", auth=(user[0]["username"], password), parameters={"email": email})
            if user:
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

                self.auth = (user["username"], password)
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

    def set_user_home(self):
        self.homes = {}
        homes = self.server_api.get("homes", auth=(self.user_authorized.username, self.user_authorized.password),
                                    parameters={"user": self.user_authorized.user_id})
        if homes:
            self.homes = {home["id"]: home for home in homes}

            if self.user_authorized.user_home:
                self.home_data_load(self.user_authorized.user_home)
            else:
                self.home_list()

    def home_list(self):
        home_list = DialogList()
        for home_id in self.homes.keys():
            home_list.add_widget(
                OneLineAvatarIconListItem(
                    IconLeftWidget(icon="home"),
                    RightRaisedButton(
                        MDIconButton(icon="delete", on_release=lambda x: self.delete_home_dialog(x))),
                    id=f"{home_id}",
                    text=self.homes[home_id]["name"],
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
            self.app_api.update_user(self.user_authorized, user_home=home_id)
        self.user_authorized.user_home = home_id
        screen_manager.screens[1].ids.home_name.title = self.homes[home_id]["name"]

        self.home_devices = self.server_api.get("home_devices",
                                                auth=self.auth,
                                                parameters={"home": home_id})

        screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
            self.home_two_line_list_widget(self.homes[home_id], self.homes[home_id]["name"], self.home_devices))

        rooms = self.server_api.get("rooms",
                                    auth=self.auth,
                                    parameters={"home": home_id})
        for room in rooms:
            self.rooms[room["id"]] = room["name"]
            self.room_devices[room["id"]] = self.server_api.get("room_devices",
                                                                auth=(self.user_authorized.username,
                                                                      self.user_authorized.password),
                                                                parameters={"room": room["id"]})
            screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
                self.room_two_line_list_widget(room, room["name"], self.room_devices[room["id"]]))

        if screen_manager.screens[1].ids.home_main.current == "Room devices":
            screen_manager.screens[1].ids.home_main.current = "Settings"

        if self.dialog:
            self.dialog_close()

    def home_two_line_list_widget(self, obj, obj_name, obj_devices):
        return TwoLineAvatarIconListItem(
            LeftRaiseButton(
                MDIconButton(icon="cog", on_release=lambda x: print("settings"))),
            text=obj_name,
            secondary_text=f"Devices: {len(obj_devices)}",
            id=f"{obj['id']}",
            on_release=lambda x: self.room_devices_list(obj_name, obj_devices))

    def room_two_line_list_widget(self, obj, obj_name, obj_devices):
        return TwoLineAvatarIconListItem(
            RightRaisedButton(
                MDIconButton(icon="delete", on_release=lambda x: self.room_delete_dialog(x, obj, obj_name))),
            LeftRaiseButton(
                MDIconButton(icon="cog", on_release=lambda x: print("settings"))),
            text=obj_name,
            secondary_text=f"Devices: {len(obj_devices)}",
            id=f"{obj['id']}",
            on_release=lambda x: self.room_devices_list(obj_name, obj_devices))

    def room_delete_dialog(self, line, obj, obj_name):
        self.dialog = MDDialog(
            title="Are you sure?",
            text=f"Do you want to delete room {obj_name}?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.delete_room(line, obj))])
        self.dialog.open()

    def delete_home_dialog(self, obj):
        self.dialog_2 = MDDialog(
            title="Are you sure?",
            text=f"Do you want to delete home {obj.parent.parent.parent.text}?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.delete_home(obj))])
        self.dialog_2.open()

    def delete_room(self, widget, obj):
        self.server_api.delete("rooms", obj["id"], auth=self.auth)
        screen_manager.screens[1].ids.bottom.ids.home_page.remove_widget(widget.parent.parent.parent)
        self.rooms.pop(obj["id"])
        self.dialog_close()

    def delete_home(self, obj):
        home_id = int(obj.parent.parent.parent.id)
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

    def room_devices_list(self, obj_name, obj_devices):
        screen_manager.screens[1].ids.room.ids.room_devices.clear_widgets()
        if obj_devices:
            for device in obj_devices:
                screen_manager.screens[1].ids.room.ids.room_devices.add_widget(
                    ThreeLineAvatarIconListItem(
                        RightRaisedButton(
                            MDIconButton(icon="minus", on_release=lambda x: print("delete"))),
                        LeftRaiseButton(
                            MDIconButton(icon="cog", on_release=lambda x: print("settings"))),
                        text=device["note"],
                        secondary_text=self.devices[device["device"]]["name"],
                        tertiary_text=self.devices[device["device"]]["model"],
                        id=f"{self.devices[device['device']]['name']}"))
        screen_manager.screens[1].ids.home_main.transition.direction = 'left'
        screen_manager.screens[1].ids.home_main.current = "Room devices"
        screen_manager.screens[1].ids.top_bar.title = f"{obj_name} devices"

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
        self.home_devices = []
        self.rooms = {}
        self.room_devices = {}

        self.field_filler()
        screen_manager.transition.direction = 'right'
        screen_manager.current = 'authorization_screen'
        screen_manager.screens[1].ids.bottom.ids.home_page.clear_widgets()
        self.dialog_close()

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
        screen_manager.screens[1].ids.bottom.ids.home_page.clear_widgets()
        name = self.dialog.content_cls.ids.name.text
        home = self.server_api.post("homes", auth=self.auth,
                                    data={"name": name,
                                          "user": self.user_authorized.user_id})
        if not name:
            self.dialog.content_cls.ids.name.error = True
        elif "non_field_errors" in home.keys():
            self.name_error()
        else:
            self.homes[home["id"]] = home
            screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
                self.home_two_line_list_widget(home, home["name"], []))
            screen_manager.screens[1].ids.home_name.title = self.homes[home["id"]]["name"]
            self.app_api.update_user(self.user_authorized, user_home=home["id"])
            self.user_authorized.user_home = home["id"]
            self.dialog_close()

    def add_room(self):
        name = self.dialog.content_cls.ids.name.text
        room = self.server_api.post("rooms", auth=self.auth,
                                    data={"name": name,
                                          "home": self.user_authorized.user_home})
        if not name:
            self.dialog.content_cls.ids.name.error = True
        elif "non_field_errors" in room.keys():
            self.name_error()
        else:
            self.rooms[room["id"]] = room
            screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
                self.room_two_line_list_widget(room, room["name"], []))
            self.dialog_close()

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
        self.server_api.delete("devices", int(obj.parent.parent.parent.id), auth=self.auth)
        self.devices.pop(int(obj.parent.parent.parent.id))
        screen_manager.screens[1].ids.bottom.ids.container.remove_widget(obj.parent.parent.parent)
        self.dialog_close()

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
            self.server_api.put("devices", device_id, auth=self.auth,
                                data={"name": device_name,
                                      "model": device_model})
            obj.parent.parent.parent.text = device_name
            obj.parent.parent.parent.secondary_text = device_model
            self.devices[device_id]["name"] = device_name
            self.devices[device_id]["model"] = device_model
        self.dialog_close()

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
    def name_error():
        Snackbar(
            text="[color='black']This name already exists![/color]",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=0.977,
            bg_color=(1, 1, 1, 1),
        ).open()
