# -*- coding: UTF-8 -*-

import kivy

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar

class AutolivActionBar(ActionBar):
    """

    """
    def __init__(self, *args, **kwargs):
        super(AutolivActionBar, self).__init__(**kwargs)






class LtsBoxLayout(BoxLayout):
    """
    Główny wygląd programu, zawierają się w nim wszystkie widgety
    """
    def __init__(self, *args, **kwargs):
        super(LtsBoxLayout, self).__init__(**kwargs)


class LtsApp(App):
    """
    Main program, tutaj dodajemy widgety do uruchomienia
    """
    def __init__(self, *args, **kwargs):
        super(LtsApp, self).__init__(**kwargs)

        self.use_kivy_settings = True  # póki co na True, ale docelowo damy False

    def build(self):
        self.title = "Symulacja procesu COP"
        Window.maximize()
        # Window.clearcolor = get_color_from_hex("#757575")
        return LtsBoxLayout()


if __name__ == '__main__':
    LtsApp().run()