from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from authorization_screen import kv_authorization, AuthorizationScreen
from main_screen import kv_bottom_navigation, MainScreen


Builder.load_string(kv_authorization + kv_bottom_navigation)

sm = ScreenManager()


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

    def build(self):
        sm.add_widget(AuthorizationScreen(name='authorization'))
        sm.add_widget(MainScreen(name='main_window'))
        sm.current = 'authorization'
        return sm

    def rememder_password(self, checkbox, value):
        if value:
            print(f"Rememder Password is on {checkbox}")
        else:
            print(f"Rememder Password is off {checkbox}")

    def log_in(self, log_in_button):
        print(f"Log In {log_in_button}")

    def forgot_password(self, button_forgot_password):
        print(f"Forgot Password {button_forgot_password}")

    def sign_up(self, button_sign_up):
        print(f"Sign Up {button_sign_up}")

    def app_exit(self):
        sm.transition.direction = 'right'
        sm.current = 'authorization'
        print("Exit")

    dialog = None

    def exit_answer(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Are you sure?",
                text="Do you want to go out?",
                buttons=[
                    MDFlatButton(
                        text="NO",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        # on_release=lambda x: self.dialog.close(),
                    ),
                    MDFlatButton(
                        text="YES",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.app_exit(),
                    ),
                ],
            )
        self.dialog.open()


MyApp().run()
