from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ObjectProperty,
    ColorProperty,
    NumericProperty,
)
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout

from .commons import *


class TaskCard(ButtonBehavior, MDBoxLayout):

    title = StringProperty()
    time = StringProperty()
    date = StringProperty()
    team = StringProperty()
    progress = NumericProperty()
    priority = ColorProperty()
    task_id = NumericProperty()
    overdue = BooleanProperty(False)
    screen_manager = ObjectProperty(None)

    def open_task_info_screen(self):
        self.screen_manager.get_screen("task_info").task = self
        make_transition(self.screen_manager, "task_info")
