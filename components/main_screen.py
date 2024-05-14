from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty


class MainScreen(Screen):
    screen_manager = ObjectProperty(None)

    def login(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.current = "login"

    def signup(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.current = "signup"
