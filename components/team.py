from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivymd.uix.menu import MDDropdownMenu

from api.team import create_team, join_team
from api.user import get_user_teams
from .commons import *


class CreateTeamScreen(Screen):
    screen_manager = ObjectProperty(None)

    def confirm_create_team(self):
        team_name = self.ids["name_field"].text
        if not team_name:
            return
        status, team_id = create_team(self.screen_manager.token, team_name)
        if not status:
            return
        join_team(self.screen_manager.token, team_id)
        self.back()

    def back(self):
        make_transition(self.screen_manager, "my_info_screen", "right")


class AddMemberScreen(Screen):
    screen_manager = ObjectProperty(None)

    def confirm_join_team(self):
        team_name = self.ids["name_field"].text
        email = self.ids["email_field"].text
        if not team_name or not email:
            return
        team_id = get_team_id_from_name(team_name.strip())
        status = add_member(self.screen_manager.token, team_id, email)
        if status:
            show_success_on_screen("Add member successfully to the team")
            self.back()
        else:
            show_error_on_screen("Error, check the info again")

    def open_available_teams_menu(self, focus, *_):
        if not focus:
            return

        teams = get_user_teams(self.screen_manager.token)
        if not teams:
            return

        menu_items = [
            {
                "text": f"Team: {team["name"]}",
                "leading_icon": "github",
                "leading_icon_color": ButtonColor,
                "on_release": lambda x=team["name"]: self.set_item(x),
            } for team in teams]

        self.menu = MDDropdownMenu(
            caller=self.ids["name_field"],
            items=menu_items,
            position="bottom",
        )
        self.menu.open()

    def set_item(self, text_item):
        self.ids["name_field"].text = text_item
        self.menu.dismiss()

    def back(self):
        make_transition(self.screen_manager, "my_info_screen", "right")
