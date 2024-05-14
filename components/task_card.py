from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.uix.list.list import MDListItem


class TaskCard(RecycleDataViewBehavior, MDBoxLayout):
    title = StringProperty()
    time = StringProperty()
    date = StringProperty()
    note = StringProperty()
    team = StringProperty()
    avatar = StringProperty()
    callback = ObjectProperty(lambda x: x)

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    # def refresh_view_attrs(self, rv, index, data):
    #     self.index = index
    #     return super().refresh_view_attrs(rv, index, data)

    # def on_touch_down(self, touch):
    #     if super().on_touch_down(touch):
    #         return True
    #     if self.collide_point(*touch.pos) and self.selectable:
    #         Clock.schedule_once(self.callback)
    #         return self.parent.select_with_touch(self.index, touch)

    # def apply_selection(self, rv, index, is_selected):
    #     self.selected = is_selected
    #     rv.data[index]["selected"] = is_selected
