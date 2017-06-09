# -*- coding: UTF-8 -*-

import kivy

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
# from kivy.utils import get_color_from_hex

class QuestionPopup(Popup):

    test_text = "Ilość modułów wyprodukowanych w APA."
    tc_text = "Ilość komór temperaturowych gdzie będą kondycjonowane moduły."
    tr_text = "Ilość Test Roomów w których będą odbywać się testy."
    wich_text = "Ilość komór Walk-in w których będą odbywać się testy."
    trunk_text = "Ilość transportów z APA na dzień."
    frq_text = "Częstotliwość dokładania modułów do TC przez technika wsparcia (ustaw 0 jeżeli moduły mają być dokłądane od razu). "

    hints = [test_text, tc_text, tr_text, wich_text, trunk_text, frq_text]

    message = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(QuestionPopup, self).__init__(**kwargs)

    def open(self, where):
        self.message.text = where

        super(QuestionPopup, self).open()


class LtsBoxLayout(BoxLayout):
    """
    Główny wygląd programu, zawierają się w nim wszystkie widgety
    """

    def __init__(self, *args, **kwargs):
        super(LtsBoxLayout, self).__init__(**kwargs)

        self.questionpopup = QuestionPopup()

    def text_print(self):
        # TODO: dokończyć pobieranie danych z textinput po naciśnieciu START
        print(self.ids.test_qty.text)

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
        # Config.set("input", "mouse", "mouse, disable_multitouch")
        # Window.clearcolor = get_color_from_hex("#757575")
        return LtsBoxLayout()


if __name__ == '__main__':
    LtsApp().run()