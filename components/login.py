from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty

from api.user import get_user_token, get_user_details
from .commons import *
from .auth import cache_token


class LoginScreen(Screen):
    screen_manager = ObjectProperty(None)

    def read_email_and_password(self):
        screen = self.ids
        email = screen["email_field"].ids["email"].text
        password = screen["password_field"].ids["password"].text
        return email, password

    def validate_login_credentials(self):
        email, password = self.read_email_and_password()
        status, token = get_user_token(email, password)
        if status:
            cache_token(token)
            self.screen_manager.token = token
            show_success_on_screen("Logged in successfully")
            self.login()

        else:
            show_error_on_screen("Either email or password is incorrect")

    def login(self):
        make_transition(self.screen_manager, "tasks")

    def back(self):
        make_transition(self.screen_manager, "main", "right")
