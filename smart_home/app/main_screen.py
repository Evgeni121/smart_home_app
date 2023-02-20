from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, ILeftBodyTouch, OneLineIconListItem
from kivymd.uix.relativelayout import MDRelativeLayout

kv_bottom_navigation = '''
<DrawerClickableItem@MDNavigationDrawerItem>:
    focus_color: "lightgrey"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "orange"
    focus_behavior: True
    _no_ripple_effect: True
    
<CheckboxTextAdd>:
    height: checkbox_add.height
    size_hint_y: None
    
    MDCheckbox:
        id: checkbox_add
        size_hint: None, None
        size: "48dp", "48dp"
        on_active: 
            text_button_add.theme_text_color = "Hint" if self.active is False else "Primary"

    MDTextButton:
        id: text_button_add
        text: "Add device to Home page"
        font_style: "Body2"
        theme_text_color: "Hint"
        pos_hint: {"center_y": .5}
        pos: checkbox_add.width - dp(5), 0
        on_release:
            checkbox_add.active = False if checkbox_add.active is True else True
            
<DeviceAdd>:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    adaptive_height: True

    MDTextField:
        id: name
        helper_text_mode: "on_error"
        pos_y: 0.9
        hint_text: "Name"
        helper_text: "Name cannot be empty"

    MDTextField:
        id: model
        pos_hint_y: 0.1
        hint_text: "Model"   
            
<DeviceSettings>:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    adaptive_height: True

    MDTextField:
        id: name
        helper_text_mode: "on_error"
        pos_y: 0.9
        hint_text: "Name"
        helper_text: "Name cannot be empty"

    MDTextField:
        id: model
        pos_hint_y: 0.1
        hint_text: "Model"   
    
    CheckboxTextAdd:
        id: check
        pos_hint: {"center_x": .50, "center_y": .40}

<RoomDevices>
    adaptive_height: True

    MDScrollView:     
        MDList:
            id: room_devices
            cols: 1
            adaptive_height: True
                
            TwoLineIconListItem:
                text: "List of devices"
                secondary_text: "Active"
    
                IconLeftWidget:
                    icon: 'devices'
    
            
<MainScreen>: 
    MDBottomNavigation:
        id: bottom_navigation
        panel_color: "orange"
        text_color_active: "black"
        text_color_normal: "#4a4939"

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Home'
            icon: 'home'
            # badge_icon: "alert"
            
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                padding: dp(5)
                pos_hint_y: .5
                size_hint_y: .9    
                
                MDScrollView:
                    MDList:
                        id: home_page
                        cols: 1
                        adaptive_height: True

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Devices'
            icon: 'devices'
            
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(5)
                padding: dp(5)
                pos_hint_y: .5
                size_hint_y: .9
        
                MDBoxLayout:
                    adaptive_height: True
                    pos_hint: {"center_x": .5}
    
                    MDIconButton:
                        icon: 'magnify'
        
                    MDTextField:
                        id: search_field
                        hint_text: 'Search device'
                        on_text: app.set_list_devices(self.text, True)
                        
                MDScrollView:
                    MDList:
                        id: container
                
            MDRaisedButton:
                text: "Add device"
                font_style: "Body2"
                theme_text_color: "Primary"
                md_bg_color: "orange"
                size_hint_x: .2
                pos_hint: {"center_x": .65, "center_y": .1}
                on_release: app.add_device_dialog()

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Settings'
            icon: 'table-settings'

            MDLabel:
                text: 'Settings'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen 4'
            text: 'History'
            icon: 'history'

            MDLabel:
                text: 'History'
                halign: 'center'
                
    MDNavigationLayout:

        MDTopAppBar:
            title: "Smart Home"
            pos_hint: {"top": 1}
            elevation: 2
            md_bg_color: "orange"
            specific_text_color: "#4a4939"
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
            right_action_items: [["exit-to-app", lambda x: app.app_exit_dialog(), "Exit"]]
                        
    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 10, 10, 0)

        MDNavigationDrawerMenu:

            MDNavigationDrawerHeader:
                title: "My Home"
                title_color: "#4a4939"
                text: "Account"
                spacing: "4dp"
                padding: "12dp", 0, 0, "56dp"

            MDNavigationDrawerLabel:
                text: "Menu"

            DrawerClickableItem:
                icon: "gmail"
                right_text: "5"
                text_right_color: "green"
                text_color: "green"
                text: "Messages"

            DrawerClickableItem:
                icon: "account-alert"
                right_text: "5"
                text_right_color: "red"
                text_color: "red"
                text: "Warnings"

            MDNavigationDrawerDivider:

            MDNavigationDrawerLabel:
                text: "Labels"
                
            MDNavigationDrawerLabel:
                icon: "information-outline"
                text: "Label"
    
            MDNavigationDrawerLabel:
                icon: "information-outline"
                text: "Label" 
'''


class MainScreen(Screen):
    pass


class DeviceAdd(MDBoxLayout):
    pass


class DeviceSettings(MDBoxLayout):
    pass


class RoomDevices(MDBoxLayout):
    pass


class CheckboxTextAdd(MDRelativeLayout):
    pass


class RightRaisedButton(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class LeftRaiseButton(ILeftBodyTouch, MDBoxLayout):
    adaptive_width = True
