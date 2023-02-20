import os
import smart_home.main_api as api

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd import images_path

from smart_home.app.authorization_screen import kv_authorization, AuthorizationScreen, DialogList, MailLine
from smart_home.app.main_screen import kv_bottom_navigation, MainScreen, DeviceAdd, RightRaisedButton, \
    LeftRaiseButton, DeviceSettings, RoomDevices


Builder.load_string(kv_authorization + kv_bottom_navigation)
sm = ScreenManager()


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.user_authorized = api.get_user_homes(user_status=1)
        self.users_remember_password = api.get_user(users_remember_password=1)
        self.devices = api.get_device()
        self.dialog = None

    def build(self):
        screen_1 = AuthorizationScreen(name='authorization_screen')
        screen_2 = MainScreen(name='main_screen')
        sm.add_widget(screen_1)
        sm.add_widget(screen_2)

        if self.user_authorized:
            sm.current = 'main_screen'
        else:
            sm.current = 'authorization_screen'
            if len(self.users_remember_password) == 1:
                sm.screens[0].ids.mail_field.ids.mail_text_field.text = self.users_remember_password[0].email
                sm.screens[0].ids.password_field.ids.password_text_field.text = self.users_remember_password[0].password
        return sm

    def on_start(self):
        for device in self.devices:
            line = TwoLineAvatarIconListItem(
                RightRaisedButton(
                    MDIconButton(icon="minus",
                                 on_release=lambda x: self.delete_device_dialog(x)
                                 )),
                LeftRaiseButton(
                    MDIconButton(icon="cog",
                                 on_release=lambda x: self.settings_dialog(x)
                                 )),
                text=device.name,
                secondary_text=device.model,
                id=f"{device.device_id}")
            sm.screens[1].ids.container.add_widget(line)
        if self.user_authorized:
            self.home_list()

    def log_in(self, email, password):
        remember_password = sm.screens[0].ids.checkbox.ids.checkbox.active
        if email:
            user = api.get_user_homes(user_email=email)
            if user:
                if password == user.password:
                    if remember_password and user not in self.users_remember_password:
                        user.remember_password = 1
                        self.users_remember_password.append(user)
                        sm.screens[0].ids.checkbox.ids.checkbox.active = False
                    user.status = 1
                    api.update_user(user)
                    self.user_authorized = user
                    sm.transition.direction = 'left'
                    sm.current = 'main_screen'
                    self.home_list()
                else:
                    print(f"Invalid Password!")
                    sm.screens[0].ids.password_field.ids.password_text_field.error = True
                    sm.screens[0].ids.mail_field.ids.mail_text_field.error = False
            else:
                sm.screens[0].ids.mail_field.ids.mail_text_field.error = True
                sm.screens[0].ids.password_field.ids.password_text_field.error = False
                print(f"Invalid Mail!")

    def home_data_load(self, home_name):
        home = api.get_home_devices(self.user_authorized.homes[home_name])
        home.rooms = api.get_wholly_home(home)
        if home.rooms:
            for room in home.rooms:
                room_devices = RoomDevices()
                for device in home.rooms[room].devices:
                    room_devices.ids.room_devices.add_widget(
                        TwoLineIconListItem(
                            text=f"{home.rooms[room].devices[device].name}",
                            secondary_text=f"{home.rooms[room].devices[device].model}"
                        )
                    )

                sm.screens[1].ids.home_page.add_widget(
                    MDExpansionPanel(
                        icon=os.path.join(images_path, "logo", "kivymd-icon-128.png"),
                        content=room_devices,
                        panel_cls=MDExpansionPanelThreeLine(
                            text=f"{home.rooms[room].name}",
                            secondary_text=f"Devices: {len(home.rooms[room].devices)}",
                            tertiary_text="No Warnings",
                        )
                    )
                )
        self.dialog_close()

    def forgot_password(self, button_forgot_password):
        print(f"Forgot Password")

    def sign_up(self, button_sign_up):
        print(f"Sign Up")

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
        self.user_authorized.status = 0
        api.update_user(self.user_authorized)
        self.user_authorized = None
        if len(self.users_remember_password) == 1:
            sm.screens[0].ids.mail_field.ids.mail_text_field.text = self.users_remember_password[0].email
            sm.screens[0].ids.password_field.ids.password_text_field.text = self.users_remember_password[0].password
        else:
            sm.screens[0].ids.mail_field.ids.mail_text_field.text = ""
            sm.screens[0].ids.password_field.ids.password_text_field.text = ""

        sm.transition.direction = 'right'
        sm.current = 'authorization_screen'
        print("Exit")
        while len(sm.screens[1].ids.home_page.children) != 0:
            sm.screens[1].ids.home_page.remove_widget(sm.screens[1].ids.home_page.children[0])
        self.dialog_close()
        return sm

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
        device_category = 1
        device_type = 1
        if not name:
            self.dialog.content_cls.ids.name.error = True
        else:
            device = api.create_device(name, model, device_category, device_type)
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
            sm.screens[1].ids.container.add_widget(line)
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

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def delete_device(self, obj):
        api.delete_device(int(obj.parent.parent.parent.id))
        sm.screens[1].ids.container.remove_widget(obj.parent.parent.parent)
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
        if len(self.users_remember_password) > 1:
            for mail in self.users_remember_password:
                dialog.add_widget(
                    MailLine(
                        id="1",
                        text=mail.email,
                        icon=f"app/data/imgs/accounts/{mail.email}.png",
                        on_release=lambda x: self.choice_mail(x.text)
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

    def choice_mail(self, text):
        sm.screens[0].ids.mail_field.ids.mail_text_field.text = text
        user = api.get_user(user_email=text)
        sm.screens[0].ids.password_field.ids.password_text_field.text = user[0].password
        self.dialog_close()
        return sm

    def home_list(self):
        dialog = DialogList()
        homes = self.user_authorized.homes
        if len(homes) > 1:
            for home in homes.values():
                dialog.add_widget(
                    MailLine(
                        id="1",
                        text=home.name,
                        icon="home",
                        on_release=lambda x: self.home_data_load(x.text)
                    ))

            self.dialog = MDDialog(
                title="My Homes",
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
        else:
            key = list(self.user_authorized.homes.keys())[0]
            self.home_data_load(key)


MyApp().run()
