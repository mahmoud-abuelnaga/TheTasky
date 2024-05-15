import os
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty, StringProperty

from api.user import get_user_details, get_user_teams
from .auth import rest_token_cache
from .commons import *


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
        make_transition(self.screen_manager, "create_team")

    def open_add_member_screen(self):
        make_transition(self.screen_manager, "add_member")

    def back(self):
        make_transition(self.screen_manager, "tasks", "right")

    def signout(self):
        rest_token_cache()
        make_transition(self.screen_manager, "main", "right")
