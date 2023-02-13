from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp

from authorization import kv_authorization, AuthorizationScreen
from bottom_navigation import kv_bottom_navigation, MainWindow


Builder.load_string(kv_authorization + kv_bottom_navigation)

sm = ScreenManager()


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

    def build(self):
        sm.add_widget(AuthorizationScreen(name='authorization'))
        sm.add_widget(MainWindow(name='main_window'))
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

    def exit(self):
        sm.transition.direction = 'right'
        sm.current = 'authorization'
        print(f"Exit")


MyApp().run()
