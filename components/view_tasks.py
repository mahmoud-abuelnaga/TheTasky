from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty, StringProperty
from datetime import datetime

from .task_info import TaskInfoScreen
from api.task import get_user_tasks
from api.team import get_team_name
from .task_card import TaskCard
from .auth import read_token
from .commons import *

from_priority_to_color = {
    1: "green",
    2: "lightgreen",
    3: "yellow",
    4: "orange",
    5: "red",
}


class TaskScreen(Screen):
    screen_manager = ObjectProperty(None)

    def on_pre_enter(self, *_):
        self.ids["tasks_container"].clear_widgets()
        token = read_token()
        tasks = get_user_tasks(token)
        self.screen_manager.token = token
        if not tasks:
            return
        for task in tasks:
            self.add_task(self.handle_task(task))

    def open_info_screen(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.current = "my_info_screen"

    def open_add_task_window(self):
        make_transition(self.screen_manager, "add_task")

    def create_task(self, task):
        self.add_task(task)

    def open_task_info_screen(self, task):
        self.screen_manager.get_screen("task_info").task = task
        make_transition(self.screen_manager, "task_info")

    def add_task(self, task):
        card = TaskCard(**task, screen_manager=self.screen_manager)
        self.ids["tasks_container"].add_widget(card)

    def handle_task(self, task):
        task_dict = {}
        task_dict["title"] = task["name"]
        dead = datetime.fromisoformat(task["deadline"])
        task_dict["time"] = dead.strftime("%H:%M")
        task_dict["date"] = dead.strftime("%d/%m/%Y")
        task_dict["team"] = get_team_name(self.screen_manager.token, task["teamID"])
        task_dict["priority"] = from_priority_to_color[task.get("priority", 1)]
        task_dict["progress"] = task["progress"] / 100
        task_dict["task_id"] = task["id"]
        now = datetime.now()
        task_dict["overdue"] = now > dead
        return task_dict
