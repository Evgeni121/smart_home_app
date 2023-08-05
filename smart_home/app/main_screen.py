from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, ILeftBodyTouch, OneLineRightIconListItem
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.selectioncontrol import MDSwitch

kv_bottom_navigation = '''
<DrawerClickableItem@MDNavigationDrawerItem>:
    focus_color: "lightgrey"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "orange"
    focus_behavior: True
    _no_ripple_effect: True
        
<MySwiper@MDSwiperItem>
    RelativeLayout:
    
        FitImage:
            source: "app/data/imgs/123.jpg"
            radius: [20,]
            
        MDBoxLayout:
            adaptive_height: True
            spacing: "12dp"
    
            MDLabel:
                text: "MDLabel"
                font_style: "H5"
                size_hint_y: None
                height: self.texture_size[1]
                pos_hint: {"center_y": .5}
                opposite_colors: True

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
    id: device_add
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    height: dp(200)
    
    MDScrollView: 
        MDList:
            MDTextField:
                id: category
                text_color_normal: "black"
                hint_text: "Category"
                helper_text_mode: "on_error"
                helper_text: "Select necessary category"
                on_focus: 
                    if self.focus: app.open_list(self)
            
            MDTextField:
                id: type
                text_color_normal: "black"
                hint_text: "Type"
                helper_text_mode: "on_error"
                helper_text: "Select necessary type"
                on_focus: 
                    if self.focus: app.open_list(self)
                      
            MDTextField:
                id: name
                text_color_normal: "black"
                hint_text: "Name"
                helper_text_mode: "on_error"
                helper_text: "Name cannot be empty"
        
            MDTextField:
                id: model
                text_color_normal: "black"
                hint_text: "Model"
                helper_text_mode: "on_error"
                helper_text: "Model cannot be empty"

<RoomChoice>:
    id: device_add
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    height: dp(130)
    
    MDTextField:
        id: room
        text_color_normal: "black"
        hint_text: "Room"
        helper_text_mode: "on_error"
        helper_text: "Select necessary room"
        on_focus: 
            if self.focus: app.choice_room_list(self)
              
    MDTextField:
        id: note
        text_color_normal: "black"
        hint_text: "Note"
        helper_text_mode: "on_error"
        helper_text: "Note cannot be empty"
                             
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

<RoomDeviceSettings>:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    adaptive_height: True
    
    MDTextField:
        id: note
        helper_text_mode: "on_error"
        pos_y: 0.9
        hint_text: "Note"
        helper_text: "Note cannot be empty"

    CheckboxTextAdd:
        id:checkbox

<DeviceProperties>:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    adaptive_height: True

    MDScrollView: 
        MDList:
            id: properties
   
<RoomAdd>:
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
        
<RoomDevices>
    adaptive_height: True

    MDScrollView:     
        MDList:
            id: room_devices
            cols: 1
                
            TwoLineIconListItem:
                text: "List of devices"
                secondary_text: "Active"
    
                IconLeftWidget:
                    icon: 'devices'

<LineWithSwitch>:
    font_style: "H6"
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    
    RightSwitch:   
        pos_hint: {"center_y": .5}  
        icon_inactive_color: "grey" 
        thumb_color_inactive: "lightgrey" 
        on_active: app.behavior(self)     

<LineWithSlider>:
    adaptive_height: True 
    padding: dp(15)
    orientation: "horizontal"
    
    MDLabel:
        id: label
        adaptive_height: True 
        font_style: "Body1"
                                      
    MDSlider:   
        hint: True
        hint_bg_color: "red"
        hint_text_color: "white"
        hint_radius: [6, 0, 6, 0]
        pos_hint: {"center_y": .5}
        value: 30
        on_active: print("Slider")

<LineWithData>:
    adaptive_height: True 
    padding: dp(15)
    orientation: "horizontal"
    
    MDLabel:
        id: text
        adaptive_height: True 
        font_style: "Body1"
    
    MDLabel:
        id: value
        adaptive_height: True 
        font_style: "H6"
        
<Home>:
    
    MDSwiper:
        size_hint_y: None
        height: root.height - dp(150)
        y: root.height - self.height - dp(75)
    
        MDSwiperItem:
            RelativeLayout:
    
                FitImage:
                    source: "app/data/imgs/123.jpg"
                    radius: [20,]
                    
                MDBoxLayout:
                    adaptive_height: True
                    orientation: "vertical"
                    pos_hint: {"center_x": 0.5, "center_y": .85}
            
                    MDLabel:
                        text: "Home"
                        font_style: "H5"
                        opposite_colors: True
                        halign: "center"
                 
                MDBoxLayout:
                    adaptive_height: True
                    orientation: "vertical"
                    pos_hint: {"center_x": 0.5, "center_y": .5}
                    
                    MDList:
                        id: list_screen_home
                        
                        LineWithSwitch:
                            text: "Home Security"
                        
                        LineWithSwitch:
                            text: "Home Door"
                            
                        LineWithSwitch:
                            text: "Outside Light"
                        
                        LineWithSwitch:
                            text: "Temperature"   
                        
                            MDSlider:  
                                adaptive_height: True 
                                hint: True
                                hint_bg_color: "red"
                                hint_text_color: "white"
                                hint_radius: [6, 0, 6, 0]
                                pos_hint: {"center_y": .0}
                                value: 30   

        MDSwiperItem:
            RelativeLayout:
    
                FitImage:
                    source: "app/data/imgs/123.jpg"
                    radius: [20,]
                    
                MDBoxLayout:
                    adaptive_height: True
                    orientation: "vertical"
                    pos_hint: {"center_x": 0.5, "center_y": .85}
            
                    MDLabel:
                        text: "Room 1"
                        font_style: "H5"
                        opposite_colors: True
                        halign: "center"
                            
        MDSwiperItem:
            RelativeLayout:
    
                FitImage:
                    source: "app/data/imgs/123.jpg"
                    radius: [20,]
                    
                MDBoxLayout:
                    adaptive_height: True
                    orientation: "vertical"
                    pos_hint: {"center_x": 0.5, "center_y": .85}
            
                    MDLabel:
                        text: "Room 2"
                        font_style: "H5"
                        opposite_colors: True
                        halign: "center"

    MDBottomAppBar:

        MDTopAppBar:
            icon: "plus"
            type: "bottom"
            on_action_button: print("Add new widget")
            mode: "free-end"  
            
<Bottom>: 
    
    MDBottomNavigation:
        id: bottom_navigation
        panel_color: "orange"
        text_color_active: "black"
        text_color_normal: "#4a4939"

        MDBottomNavigationItem:
            name: 'screen_1'
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
            name: 'screen_2'
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
        
                    MDIconButton:
                        icon: 'magnify'
        
                    MDTextField:
                        id: search_field
                        hint_text: 'Search device'
                        on_text: app.set_list_devices(self.text, True)
                       
                MDScrollView:
                    MDList:
                        id: container

        MDBottomNavigationItem:
            name: 'screen_3'
            text: 'Settings'
            icon: 'table-settings'

            MDLabel:
                text: 'Settings'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen_4'
            text: 'History'
            icon: 'history'

            MDLabel:
                text: 'History'
                halign: 'center'
        
    MDFloatingActionButton:
        id: round_button
        icon: "plus"
        pos_hint: {"center_x": .8, "center_y": .2}
        on_release: 
            if bottom_navigation.previous_tab.name == "screen_2": app.add_device_dialog()
            elif bottom_navigation.previous_tab.name == "screen_1": app.add_room_dialog("Room")
            elif bottom_navigation.previous_tab.name == "screen_3": print("Add new algorithm")
            elif bottom_navigation.previous_tab.name == "screen_4": print("Add new parameter")

<Room>:
        
    MDBoxLayout:
        orientation: 'vertical'
        pos_hint_y: .5
        size_hint_y: .9  
                
        MDScrollView:
            MDList:
                id: room_devices
                                                
        MDBottomAppBar:
    
            MDTopAppBar:
                icon: "plus"
                type: "bottom"
                on_action_button: print("!")
                mode: "free-end"  

    MDFloatingActionButton:
        id: round_button
        adaptive_height: True
        adaptive_weight: True
        icon: "arrow-left-bold"
        pos_hint: {"center_x": .5, "center_y": .1}
        on_release: 
            app.change_screen("Settings")                   
                           
<MainScreen>:
                
    ScreenManager:
        id: home_main
        
        Home:
            id: home 
            name: "Home Page"
            
        Bottom:
            id: bottom
            name: "Settings"
    
        Room:
            id: room
            name: "Room devices"
            
    MDNavigationLayout:

        MDTopAppBar:
            id: top_bar
            title: f"{home_name.title}: {home_main.current}"
            pos_hint: {"top": 1}
            elevation: 2
            md_bg_color: "orange"
            specific_text_color: "#4a4939"
            left_action_items: 
                [["menu", lambda x: nav_drawer.set_state("open")]]
            right_action_items: 
                [["home", lambda x: app.home_list(), "My Homes"],
                ["exit-to-app", lambda x: app.app_exit_dialog(), "Exit"]]
            
    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 10, 10, 0)

        MDNavigationDrawerMenu:

            MDNavigationDrawerHeader:
                id: home_name
                title: "Select or create home!"
                title_color: "#4a4939"
                text: home_main.current
                spacing: "4dp"
                padding: "12dp", 0, 0, "56dp"

            MDNavigationDrawerLabel:
                text: "Menu"

            DrawerClickableItem:
                id: home_page_control
                icon: "home"
                text_color: "black"
                text: "Home Page"
                on_release: 
                    home_main.transition.direction = 'left'
                    home_main.current = "Home Page"
                    nav_drawer.set_state("close")

            DrawerClickableItem:
                icon: "format-list-group-plus"
                text_color: "black"
                text: "Settings"
                on_release: 
                    home_main.transition.direction = 'left'
                    home_main.current = "Settings"
                    nav_drawer.set_state("close")
            
            MDNavigationDrawerDivider:
'''


class MainScreen(Screen):
    pass


class Bottom(Screen):
    pass


class Home(Screen):
    pass


class Room(Screen):
    pass


class Scr(Screen):
    pass


class DeviceAdd(MDBoxLayout):
    pass


class RoomChoice(MDBoxLayout):
    pass


class RoomAdd(MDBoxLayout):
    def __init__(self, name, *args):
        super().__init__(*args)
        self.my_name = name
    pass


class DeviceSettings(MDBoxLayout):
    pass


class RoomDeviceSettings(MDBoxLayout):
    pass


class DeviceProperties(MDBoxLayout):
    pass


class RoomDevices(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class CheckboxTextAdd(MDRelativeLayout):
    pass


class RightRaisedButton(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class LeftRaiseButton(ILeftBodyTouch, MDBoxLayout):
    adaptive_width = True


class LineWithSwitch(OneLineRightIconListItem):
    icon = StringProperty()


class LineWithSlider(MDBoxLayout):
    pass


class LineWithData(MDBoxLayout):
    pass


class RightSwitch(IRightBodyTouch, MDSwitch):
    active: False
