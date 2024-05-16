import os

# os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.lang import Builder
from kivy.core import window
from kivymd.app import MDApp

from components.add_task import AddTaskScreen
from components.login import LoginScreen
from components.signup import SignupScreen
from components.view_tasks import TaskScreen
from components.main_screen import MainScreen
from components.user_info import InfoScreen
from components.task_info import TaskInfoScreen
from components.team import CreateTeamScreen, AddMemberScreen
from components.auth import is_valid_token, read_token
from components.commons import *


class App(MDApp):
    def build(self):
        window.Window.clearcolor = "#252525"
        self.sm = Builder.load_file("./kvfiles/app.kv")
        # bypass login if token is cached
        self.bypass_login()
        return self.sm

    def bypass_login(self):
        token = read_token()
        if not is_valid_token(token):
            return

        self.sm.current = "tasks"
        self.sm.token = token

    def on_start(self, *_):
        pass

if __name__ == "__main__":
    App().run()
