from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty
from asynckivy import sleep


from api.user import create_user
from .commons import show_error_on_screen, show_success_on_screen


class SignupScreen(Screen):
    screen_manager = ObjectProperty(None)

    def read_info(self):
        screen = self.ids
        name = screen["name_field"].ids["name"].text
        email = screen["email_field"].ids["email"].text
        password = screen["password_field"].ids["password"].text
        return name, email, password

    def signup(self):
        name, email, password = self.read_info()
        status = create_user(name, email, password)
        if status:
            show_success_on_screen("User is registered successfully")
            sleep(1)
            self.login()
        else:
            show_error_on_screen("User is already registered")

    def login(self):
        make_transition(self.screen_manager, "login")

    def back(self):
        make_transition(self.screen_manager, "main", "right")
