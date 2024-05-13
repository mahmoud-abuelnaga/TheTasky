from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty, StringProperty

from api.user import get_user_details, get_user_teams
from .commons import TOKEN, TOKEN_CHANGED

class InfoScreen(Screen):
    screen_manager = ObjectProperty(None)
    name = StringProperty("")
    email = StringProperty("")
    token = StringProperty("")


    def on_pre_enter(self, *args):
        global TOKEN_CHANGED
        print("self.token", self.token)
        if TOKEN_CHANGED:
            self.name, self.email = get_user_details(self.token)
            TOKEN_CHANGED = False
        # get_user_teams(self.token)

    def back(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.transition.direction = "right"
        self.screen_manager.current = "tasks"

    def signout(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.transition.direction = "right"
        self.screen_manager.current = "main"
