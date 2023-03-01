from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu

from smart_home.app.authorization_screen import AuthorizationScreen, DialogList, MailLine, kv_authorization
from smart_home.app.main_screen import MainScreen, DeviceAdd, RightRaisedButton, \
    LeftRaiseButton, DeviceSettings, kv_bottom_navigation

from smart_home.app.database import app_api

Builder.load_string(kv_authorization + kv_bottom_navigation)
screen_manager = ScreenManager()


class SmartHome(MDApp):
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
        self.devices = server_api.get("devices")

        self.homes = None
        self.home_devices = None
        self.rooms = None
        self.room_devices = None
        self.user_devices = None
        self.server_api = server_api
        self.app_api = app_api
        self.dialog = None
        self.menu = None

    def build(self):
        screen_1 = AuthorizationScreen(name='authorization_screen')
        screen_2 = MainScreen(name='main_screen')
        screen_manager.add_widget(screen_1)
        screen_manager.add_widget(screen_2)

        if self.user_authorized:
            screen_manager.current = 'main_screen'
        else:
            screen_manager.current = 'authorization_screen'
            self.filler()
        return screen_manager

    def on_start(self):
        self.set_list_devices()

        if self.user_authorized:
            self.set_user_home()

    def set_list_devices(self, text="", search=False):
        def add_widget(available_device):
            screen_manager.screens[1].ids.bottom.ids.container.add_widget(
                TwoLineAvatarIconListItem(
                    RightRaisedButton(
                        MDIconButton(icon="minus",
                                     on_release=lambda x: self.delete_device_dialog(x)
                                     )),
                    LeftRaiseButton(
                        MDIconButton(icon="cog",
                                     on_release=lambda x: self.settings_dialog(x)
                                     )),
                    text=available_device["name"],
                    secondary_text=available_device["model"],
                    id=f"{available_device['id']}"
                )
            )

        screen_manager.screens[1].ids.bottom.ids.container.clear_widgets()

        for device in self.devices:
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
        if self.user_authorized:
            if self.user_authorized.user_home:
                self.home_data_load(self.user_authorized.user_home)
            else:
                self.home_list()

    def home_list(self):
        homes = self.server_api.get("homes", auth=(self.user_authorized.username,
                                                   self.user_authorized.password),
                                    parameters={"user": self.user_authorized.user_id})
        if homes:
            home_names = {}
            for home in homes:
                home_names[home["id"]] = home["name"]
            self.homes = home_names
            home_list = DialogList()
            for home_id in home_names.keys():
                home_list.add_widget(
                    MailLine(
                        id=f"{home_id}",
                        text=home_names[home_id],
                        icon="home",
                        on_release=lambda x: self.home_data_load(x.id, home_name=x.text)
                    ))

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
                        on_release=self.dialog_close,
                    )
                ]
            )
            self.dialog.open()

    def home_data_load(self, home_id, home_name=None):
        screen_manager.screens[1].ids.bottom.ids.home_page.clear_widgets()
        self.app_api.update_user(self.user_authorized, user_home=home_id)
        self.user_authorized.user_home = home_id
        self.home_devices = self.server_api.get("home_devices",
                                                auth=(self.user_authorized.username, self.user_authorized.password),
                                                parameters={"home": home_id})
        # self.rooms =
        #
        # home.rooms = self.api.get_wholly_home(home)
        # self.user_active_home = home
        # screen_manager.screens[1].ids.home_name.title = home.name
        # if home.devices:
        #     screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
        #         self.two_line_list(home, home.name, home.devices)
        #     )
        # if home.rooms:
        #     for room in home.rooms:
        #         screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
        #             self.two_line_list(home.rooms[room], home.rooms[room].name, home.rooms[room].devices)
        #         )
        if self.dialog:
            self.dialog_close()

    def two_line_list(self, obj, obj_name, obj_devices):
        return TwoLineAvatarIconListItem(
            RightRaisedButton(
                MDIconButton(icon="minus", on_release=lambda x: print("delete"))),
            LeftRaiseButton(
                MDIconButton(icon="cog", on_release=lambda x: print("settings"))),
            text=obj_name,
            secondary_text=f"Devices: {len(obj_devices)}",
            id=f"{obj_name}",
            on_release=lambda x: self.room_devices(obj, obj_devices)
        )

    def app_exit_dialog(self):
        self.dialog = MDDialog(
            title="Are you sure?",
            text="Do you want to go out?",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_close,
                ),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.app_exit(),
                ),
            ],
        )
        self.dialog.open()

    def app_exit(self):
        self.app_api.update_user(self.user_authorized, user_authorized=False)
        if not self.user_authorized.user_remember_password:
            self.app_api.delete_user(self.user_authorized)
        self.user_authorized = None

        self.filler()
        screen_manager.transition.direction = 'right'
        screen_manager.current = 'authorization_screen'
        screen_manager.screens[1].ids.bottom.ids.home_page.clear_widgets()
        self.dialog_close()
        return screen_manager

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
                    on_release=self.dialog_close,
                ),
                MDRaisedButton(
                    text="ADD",
                    theme_text_color="Hint",
                    on_release=lambda x: self.add_device(),
                ),
            ],
        )
        self.dialog.open()

    def add_device(self):
        name = self.dialog.content_cls.ids.name.text
        model = self.dialog.content_cls.ids.model.text
        device_category = self.dialog.content_cls.ids.category.id
        device_type = self.dialog.content_cls.ids.type.id
        if not name:
            self.dialog.content_cls.ids.name.error = True
        elif not device_category:
            self.dialog.content_cls.ids.category.error = True
        elif not device_type:
            self.dialog.content_cls.ids.type.error = True
        else:
            device = self.api.create_device(name=name,
                                            model=model,
                                            category=int(device_category),
                                            type=int(device_type))
            self.devices.append(device)
            line = TwoLineAvatarIconListItem(
                RightRaisedButton(
                    MDIconButton(icon="minus",
                                 on_release=lambda x: self.delete_device_dialog(x))),
                LeftRaiseButton(
                    MDIconButton(icon="cog",
                                 on_release=lambda x: self.settings_dialog(x))),
                text=name,
                secondary_text=model,
                id=f"{device.device_id}")
            screen_manager.screens[1].ids.bottom.ids.container.add_widget(line)
            self.dialog_close()

    def add_room_dialog(self):
        name = "12345"
        self.api.create_room(self.user_active_home, name)
        home = self.user_active_home
        screen_manager.screens[1].ids.bottom.ids.home_page.add_widget(
            self.two_line_list(home.rooms[name], home.rooms[name].name, home.rooms[name].devices))

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
                    on_release=self.dialog_close,
                ),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Hint",
                    on_release=lambda x: self.delete_device(obj),
                ),
            ],
        )
        self.dialog.open()

    def delete_device(self, obj):
        self.api.delete_device(int(obj.parent.parent.parent.id))
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
                    on_release=self.dialog_close,
                ),
                MDRaisedButton(
                    text="SAVE",
                    theme_text_color="Hint",
                    on_release=lambda x: self.device_setting(primary_name, primary_model, device_settings, obj),
                ),
            ],
        )
        self.dialog.open()

    def device_setting(self, primary_device_name, primary_model, device_settings, obj):
        device_name = device_settings.ids.name.text
        device_model = device_settings.ids.model.text

        if primary_device_name != device_name and primary_model != device_model:
            ...

        add_device_to_home_page = self.dialog.content_cls.ids.check.ids.checkbox_add.active
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
                        on_release=lambda x: self.choice_mail(x.text, x.id)
                    ))

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
                        on_release=self.dialog_close,
                    )
                ]
            )
            self.dialog.open()

    def choice_mail(self, text, user_id):
        screen_manager.screens[0].ids.mail_field.ids.mail_text_field.text = text
        screen_manager.screens[0].ids.password_field.ids.password_text_field.text = self.users[int(user_id)].password
        self.dialog_close()

    def open_list(self, obj):
        if obj.hint_text == "Type":
            object_dict = self.devices[0].TYPE
        else:
            object_dict = self.devices[0].CATEGORY
        menu_items = [
            {
                "id": f"{i}",
                "text": f"{object_dict[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{object_dict[i]}": self.menu_callback(x, obj, i),
            } for i in range(1, len(object_dict) + 1)
        ]
        self.menu = MDDropdownMenu(
            caller=obj,
            items=menu_items,
            position="bottom",
            width_mult=4,
            max_height=dp(200),
        )
        self.menu.open()

    def menu_callback(self, text_item, obj, i):
        obj.text = text_item
        obj.id = str(i)
        self.menu.dismiss()

    def filler(self):
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

    @staticmethod
    def room_devices(obj, obj_devices):
        screen_manager.screens[1].ids.room.ids.room_devices.clear_widgets()
        if obj_devices:
            for device in obj_devices:
                screen_manager.screens[1].ids.room.ids.room_devices.add_widget(
                    TwoLineAvatarIconListItem(
                        RightRaisedButton(
                            MDIconButton(icon="minus", on_release=lambda x: print("delete"))),
                        LeftRaiseButton(
                            MDIconButton(icon="cog", on_release=lambda x: print("settings"))),
                        text=obj_devices[device].name,
                        secondary_text=obj_devices[device].model,
                        id=f"{obj_devices[device].name}"
                    )
                )
        screen_manager.screens[1].ids.home_main.transition.direction = 'left'
        screen_manager.screens[1].ids.home_main.current = "Room devices"
        screen_manager.screens[1].ids.top_bar.title = f"{obj.name} devices"
        print(obj.name)

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
