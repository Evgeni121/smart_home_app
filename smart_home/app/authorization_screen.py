from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem

kv_authorization = '''   
<MailLine>:
    IconLeftWidget:
        icon: root.icon
        
<DialogList>:
    orientation: "vertical"
    spacing: "5dp"
    size_hint_y: None
    adaptive_height: True
        
<MailField>:
    size_hint_y: None
    height: mail_text_field.height
    text: mail_text_field.text
    
    MDTextField
        id: mail_text_field
        text_color_normal: "black"
        helper_text_mode: "on_error"
        # validator: "email"
        hint_text: "Email"
        helper_text: "user@mail.ru"
        icon_left: "email"
        # on_release: app.mail_list()
        
    MDDropDownItem:
        id: drop_down_item
        pos_hint: {'center_y': .5}
        pos: mail_text_field.width - self.width,0
        on_release: app.mail_list()
                                    
<PasswordField>:
    size_hint_y: None
    height: password_text_field.height
    text: password_text_field.text
    
    MDTextField:
        id: password_text_field
        text_color_normal: "black"
        helper_text_mode: "on_error"
        hint_text: "Password"
        helper_text: "Password is wrong"
        password: True
        error: False
        icon_left: "key-variant"

    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .5}
        pos: password_text_field.width - self.width + dp(8), 0
        theme_text_color: "Hint"
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            password_text_field.password = False if password_text_field.password is True else True

<RememderPasswordCheckbox>:
    height: checkbox.height
    size_hint_y: None
    
    MDCheckbox:
        id: checkbox
        size_hint: None, None
        size: "48dp", "48dp"
        on_active: 
            text_button.theme_text_color = "Hint" if self.active is False else "Primary"

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
        id: authorization
        radius: [400, 0, 400, 0]
        md_bg_color: "#f6eeee"

        MDLabel:
            text: "Smart Home"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: "orange"
            pos_hint: {"center_y": .9} 

        MDSmartTile:
            radius: 24
            box_radius: [0, 0, 0, 0]
            box_color: 0, 0, 0, 0
            source: "app/data/imgs/devices.png"
            pos_hint: {"center_x": .5, "center_y": .77}
            size_hint: None, None
            size: "150dp", "150dp"

        MailField:
            id: mail_field
            size_hint_x: .8
            pos_hint: {"center_x": .5, "center_y": .6}

        PasswordField:
            id: password_field
            size_hint_x: .8
            pos_hint: {"center_x": .5, "center_y": .5}

        RememderPasswordCheckbox:
            id: checkbox
            pos_hint: {"center_x": .57, "center_y": .41}

        MDRaisedButton:
            text: "Log In"
            font_style: "H6"
            theme_text_color: "Hint"
            md_bg_color: "orange"
            size_hint_x: .7
            pos_hint: {"center_x": .5, "center_y": .3}
            on_release: app.log_in(mail_field.text, password_field.text)

        MDTextButton:
            text: "Forgot password?"
            theme_text_color: "Custom"
            text_color: "green"
            font_style: "Body2"
            pos_hint: {"center_x": .5, "center_y": .22}
            on_release: app.forgot_password(*args)

        MDFlatButton:
            text: "Sign Up"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: "orange"
            pos_hint: {"center_x": .5, "center_y": .14}
            on_release: app.sign_up(*args)   
        
        MDLabel:
            text: "2023"
            halign: "center"
            font_style: "Caption"
            theme_text_color: "Hint"
            pos_hint: {"center_y": .05} 
'''


class AuthorizationScreen(Screen):
    pass


class MailField(MDRelativeLayout):
    pass


class PasswordField(MDRelativeLayout):
    pass


class RememderPasswordCheckbox(MDRelativeLayout):
    pass


class DialogList(MDBoxLayout):
    pass


class MailLine(OneLineIconListItem):
    icon = StringProperty()
