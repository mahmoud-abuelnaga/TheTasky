from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty

from .commons import *
from api.task import delete_task, update_task


class TaskInfoScreen(Screen):
    screen_manager = ObjectProperty(None)
    task = ObjectProperty(None)

    def update_progress(self):
        current = self.ids["progress_field"].value
        if current / 100 == self.task.progress:
            return
        status = update_task(
            self.screen_manager.token, self.task.task_id, "progress", current
        )
        if status:
            self.back()

    def complete_task(self):
        status = update_task(
            self.screen_manager.token, self.task.task_id, "status", "done"
        )
        if status:
            self.back()

    def delete_task(self):
        status = delete_task(self.screen_manager.token, self.task.task_id)
        if status:
            self.back()
        show_error_on_screen("Error Deleting task")

    def back(self):
        make_transition(self.screen_manager, "tasks", "right")
