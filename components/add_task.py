from datetime import datetime, date
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import (
    MDTimePickerDialVertical,
    MDDockedDatePicker,
    MDModalDatePicker,
)
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText


from api.user import get_user_teams
from api.team import get_team_members
from api.task import create_task
from .commons import *


class AddTaskScreen(Screen):
    screen_manager = ObjectProperty(None)
    team_id = ObjectProperty(None)
    member_id = ObjectProperty(None)

    def on_select_day(self, instance_date_picker, number_day):
        instance_date_picker.dismiss()
        MDSnackbar(
            MDSnackbarSupportingText(
                text=f"The selected day is {number_day}",
            ),
            y=dp(24),
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            background_color="olive",
        ).open()

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
                "on_release": lambda x=team: self.set_team_name(x),
            } for team in teams]

        self.team_menu = MDDropdownMenu(
            caller=self.ids["team_field"],
            items=menu_items,
            position="bottom",
        )
        self.team_menu.open()

    def set_team_name(self, team):
        self.ids["team_field"].text = team["name"]
        self.team_id = team["id"]
        self.team_menu.dismiss()

    def open_team_members_menu(self, focus, *_):
        if not focus or self.team_id is None:
            return

        members = get_team_members(self.screen_manager.token, self.team_id)
        if not members:
            return

        menu_items = [
            {
                "text": f"Member: {member["name"]}",
                "leading_icon": "github",
                "leading_icon_color": ButtonColor,
                "on_release": lambda x=member: self.set_member_name(x),
            } for member in members]

        self.member_menu = MDDropdownMenu(
            caller=self.ids["assigned_to_field"],
            items=menu_items,
            position="bottom",
        )
        self.member_menu.open()

    def set_member_name(self, member):
        self.ids["assigned_to_field"].text = member["name"]
        self.member_id = member["id"]
        self.member_menu.dismiss()

    def read_task_info(self):
        data_to_id = {
            "title": "title_field",
            "note": "note_field",
            "time": "time_field",
            "date": "date_field",
            "team": "team_field",
            "assigned_to": "assigned_to_field",
        }

        data = {}
        for key, value in data_to_id.items():
            data[key] = self.ids[value].text

        data["priority"] = int(self.ids["priority_field"].value)
        return data

    def map_to_db_task(self, task):

        dt = datetime.strptime(task["date"], "%d/%m/%Y")
        t = datetime.strptime(task["time"], "%H:%M").time()
        dt = dt.combine(dt, t).isoformat()

        return {
            "name": str(task["title"]),
            "priority": int(task["priority"]),
            "teamID": int(self.team_id),
            "assignedToID": int(self.member_id),
            "deadline": dt,
        }

    def create_task(self):
        task = self.read_task_info()
        task_db = self.map_to_db_task(task)
        status = create_task(self.screen_manager.token, task_db)
        if status:
            screen = self.screen_manager.get_screen("tasks")
            # screen.add_task(task)
            self.back()

    def date_on_ok(self, picker, *_):
        date = picker.get_date()[0].strftime("%d/%m/%Y")
        self.ids["date_field"].text = date
        picker.dismiss()

    def time_on_ok(self, picker, *_):
        time = picker.time.strftime("%H:%M")
        self.ids["time_field"].text = time
        picker.dismiss()

    def on_cancel(self, picker, *_):
        picker.dismiss()

    def show_time_picker(self, focus):
        if not focus:
            return
        time_picker = MDTimePickerDialVertical()
        time_picker.bind(on_cancel=self.on_cancel, on_ok=self.time_on_ok)
        time_picker.open()

    def show_date_picker(self, focus):
        if not focus:
            return
        date_dialog = MDModalDatePicker(min_date=date.today())
        date_dialog.bind(on_cancel=self.on_cancel, on_ok=self.date_on_ok)
        date_dialog.open()

    def back(self):
        make_transition(self.screen_manager, "tasks", "right")
