from kivy.uix.screenmanager import Screen

from kivymd.uix.scrollview import MDScrollView


kv_bottom_navigation = '''
<DrawerClickableItem@MDNavigationDrawerItem>:
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"
    focus_behavior: True
    _no_ripple_effect: True
                
<MainScreen>:
    # MDBottomNavigation:
    #     panel_color: "orange"
    #     elevation: 4
    #     # selected_color_background: "orange"
    #     text_color_active: "black"
    #     text_color_normal: "grey"
    # 
    #     MDBottomNavigationItem:
    #         name: 'screen 1'
    #         text: 'Home'
    #         icon: 'home'
    #         # badge_icon: "alert"
    # 
    #         MDLabel:
    #             text: 'Home'
    #             halign: 'center'
    # 
    #     MDBottomNavigationItem:
    #         name: 'screen 2'
    #         text: 'Devices'
    #         icon: 'devices'
    # 
    #         MDLabel:
    #             text: 'Devices'
    #             halign: 'center'
    # 
    #     MDBottomNavigationItem:
    #         name: 'screen 3'
    #         text: 'Settings'
    #         icon: 'table-settings'
    # 
    #         MDLabel:
    #             text: 'Settings'
    #             halign: 'center'
    #             
    #     MDBottomNavigationItem:
    #         name: 'screen 4'
    #         text: 'History'
    #         icon: 'history'
    # 
    #         MDLabel:
    #             text: 'History'
    #             halign: 'center'
                
    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

                MDTopAppBar:
                    title: "Smart Home"
                    pos_hint: {"top": 1}
                    md_bg_color: "orange"
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    right_action_items: [["exit-to-app", lambda x: app.exit_answer(), "Exit"]]

    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 16, 16, 0)

        MDNavigationDrawerMenu:

            MDNavigationDrawerHeader:
                title: "My Home"
                title_color: "#4a4939"
                text: "Control"
                spacing: "4dp"
                padding: "12dp", 0, 0, "56dp"

            MDNavigationDrawerLabel:
                text: "Menu"

            DrawerClickableItem:
                icon: "gmail"
                # right_text: "+99"
                # text_right_color: "#4a4939"
                text: "Messages"

            DrawerClickableItem:
                icon: "account-alert"
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


class ContentNavigationDrawer(MDScrollView):
    pass


class MainScreen(Screen):
    pass
