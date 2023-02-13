from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.screenmanager import Screen


kv_authorization = '''                   
<ClickableTextFieldRound>:
    size_hint_y: None
    height: text_field.height

    MDTextField:
        id: text_field
        helper_text: "Password is wrong"
        helper_text_mode: "on_error"
        hint_text: "Password"
        text: root.text
        password: True
        icon_left: "key-variant"

    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .5}
        pos: text_field.width - self.width + dp(8), 0
        theme_text_color: "Hint"
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            text_field.password = False if text_field.password is True else True

<CheckboxText>:
    height: text_button.height

    MDCheckbox:
        id: checkbox
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {'center_y': .5}
        on_active: 
            text_button.theme_text_color = "Hint" if self.active is False else "Primary"
            app.rememder_password(*args)

    MDTextButton:
        id: text_button
        text: "Remember password"
        font_style: "Body2"
        theme_text_color: "Hint"
        pos_hint: {"center_y": .5}
        pos: checkbox.width - dp(5), 0
        on_release:
            checkbox.active = False if checkbox.active is True else True

<AuthorizationScreen>:
    MDScreen:
        radius: [400, 0, 400, 0]
        md_bg_color: "#f6eeee"

        MDLabel:
            id:main_label
            text: "Smart Home App"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: "orange"
            pos_hint: {"center_y": .9} 

        MDSmartTile:
            radius: 24
            box_radius: [0, 0, 0, 0]
            box_color: 0, 0, 0, 0
            source: "smart_home.png"
            pos_hint: {"center_x": .5, "center_y": .77}
            size_hint: None, None
            size: "150dp", "150dp"

        MDTextField:
            id: mail
            hint_text: "Email"
            helper_text: "user@mail.ru"
            validator: "email"
            pos_hint: {"center_x": .5, "center_y": .60}
            size_hint_x: .8
            icon_left: "email"

        ClickableTextFieldRound:
            size_hint_x: .8
            pos_hint: {"center_x": .5, "center_y": .50}

        CheckboxText:
            pos_hint: {"center_x": .57, "center_y": .42}

        MDRaisedButton:
            id: log_in_button
            text: "Log In"
            font_style: "H6"
            theme_text_color: "Hint"
            md_bg_color: "orange"
            halign: "center"
            valign: "center"
            size_hint_x: .7
            size_hint_y: .07
            pos_hint: {"center_x": .5, "center_y": .3}
            on_release: app.log_in(*args)
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'main_window'

        MDTextButton:
            id: button_forgot_password
            text: "Forgot password?"
            theme_text_color: "Custom"
            text_color: "green"
            font_style: "Body2"
            pos_hint: {"center_x": .5, "center_y": .22}
            on_release: app.forgot_password(*args)

        MDLabel:
            text: "2023"
            halign: "center"
            font_style: "Caption"
            theme_text_color: "Hint"
            pos_hint: {"center_y": .05} 

        MDFlatButton:
            id: button_sign_up
            text: "Sign Up"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: "orange"
            pos_hint: {"center_x": .5, "center_y": .14}
            on_release: app.sign_up(*args)   
'''


class AuthorizationScreen(Screen):
    pass


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    # Here specify the required parameters for MDTextFieldRound:
    # [...]


class CheckboxText(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    # Here specify the required parameters for MDTextFieldRound:
    # [...]
