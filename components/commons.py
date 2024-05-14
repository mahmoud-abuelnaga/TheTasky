from asyncio import shield
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import ColorProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText, MDSnackbarText

ButtonColor = "#2992b5"


class SelectableRecycleGridLayout(
    FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout
):
    pass


class EmailField(MDRelativeLayout):
    text = StringProperty()


class PasswordField(MDRelativeLayout):
    text = StringProperty()

    def on_text(self, instance, text):
        if len(text) < 5:
            self.error = True


class NameField(MDRelativeLayout):
    text = StringProperty()


class TeamBadge(MDBoxLayout):
    team = StringProperty()
    color = ColorProperty()


class BackButton(MDRelativeLayout):
    screen = ObjectProperty(None)

    def back(self):
        self.screen.back()


def show_msg_on_screen_base(msg, bg_color):
    MDSnackbar(
        MDSnackbarText(
            text=msg,
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color="black",
        ),
        y=dp(24),
        orientation="horizontal",
        pos_hint={"center_x": 0.5},
        size_hint_x=0.5,
        background_color=bg_color,
    ).open()


def show_error_on_screen(error_msg):
    show_msg_on_screen_base(error_msg, "red")


def show_success_on_screen(msg):
    show_msg_on_screen_base(msg, "lightgreen")
