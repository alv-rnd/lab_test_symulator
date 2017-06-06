# -*- coding: UTF-8 -*-

import kivy

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout


class LtsApp(App):
    """
    Main program, tutaj dodajemy widgety do uruchomienia
    """
    def __init__(self, *args, **kwargs):
        super(LtsApp, self).__init__(**kwargs)

        self.use_kivy_settings = True  # póki co na True, ale docelowo damy False
