from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.metrics import dp

from kivymd.uix.pickers import (
    MDTimePickerDialVertical,
    MDDockedDatePicker,
    MDModalDatePicker,
)
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText

import datetime


class AddTaskScreen(Screen):
    screen_manager = ObjectProperty(None)

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

    def create_task(self):
        task = self.read_task_info()
        # TODO: add task to database
        screen = self.screen_manager.get_screen("tasks")
        screen.add_task(task)
        self.back()

    def date_on_ok(self, picker, *_):
        date = picker.get_date()[0].strftime("%d/%m/%Y")
        self.ids["date_field"].text = date
        picker.dismiss()

    def time_on_ok(self, picker, *_):
        time = picker.time.strftime("%H:%M")
        print(time)
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
        date_dialog = MDModalDatePicker(min_date=datetime.date.today())
        date_dialog.bind(on_cancel=self.on_cancel, on_ok=self.date_on_ok)
        date_dialog.open()

    def back(self):
        self.screen_manager.transition = SlideTransition()
        self.screen_manager.transition.direction = "right"
        self.screen_manager.current = "tasks"
