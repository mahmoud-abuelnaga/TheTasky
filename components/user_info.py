import os
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty, StringProperty

from api.user import get_user_details, get_user_teams
from .auth import rest_token_cache


class InfoScreen(Screen):
    screen_manager = ObjectProperty(None)
    user_name = StringProperty("")
    email = StringProperty("")
    token = StringProperty("")

    def on_pre_enter(self, *args):
        token = self.screen_manager.token
        self.user_name, self.email = get_user_details(token)
        # get_user_teams(self.token)

    def open_create_team_screen(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.current = "create_team"

    def back(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.transition.direction = "right"
        self.screen_manager.current = "tasks"

    def signout(self):
        rest_token_cache()
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.transition.direction = "right"
        self.screen_manager.current = "main"
