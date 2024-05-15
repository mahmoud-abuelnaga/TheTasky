from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty

from .commons import *


class MainScreen(Screen):
    screen_manager = ObjectProperty(None)

    def login(self):
        make_transition(self.screen_manager, "login")

    def signup(self):
        make_transition(self.screen_manager, "signup")
