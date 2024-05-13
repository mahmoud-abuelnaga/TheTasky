from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty, StringProperty

from datetime import datetime

from api.task import get_user_tasks, get_team
from .task_card import TaskCard


class TaskScreen(Screen):
    screen_manager = ObjectProperty(None)
    token = StringProperty("")

    def on_pre_enter(self, *_):
        pass 
        # tasks = get_user_tasks(self.token)
        # if not tasks:
        #     return
        # for task in tasks:
        #     self.add_task(self.handle_task(task))

    def open_info_screen(self):
        print(self.screen_manager.screens)
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.current = "my_info_screen"

    def open_add_task_window(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.current = "add_task"

    def create_task(self, task):
            
        self.add_task(task)

    def add_task(self, task):
        self.ids["tasks_container"].add_widget(
            TaskCard(
                title = task["title"],
                note = task["note"],
                time = task["time"],
                date = task["date"],
                team = task["team"]
            )
        )
    def handle_task(self, task):
        task_dict = {}
        task_dict["title"] = task["name"]
        task_dict["priority"] = task["priority"]
        deadline = datetime(task["deadline"])
        task_dict["time"] = deadline.strftime("%H:%M")
        task_dict["date"] = deadline.strftime("%d/%m/%Y")
        task_dict["team"] = get_team(self.token, task["teamID"])
        return task_dict