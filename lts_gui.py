# -*- coding: UTF-8 -*-

import kivy

import LTS

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import kivy.garden.matplotlib
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty
# from kivy.utils import get_color_from_hex


class Graph_1(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_1, self).__init__(**kwargs)


class Graph_2(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_2, self).__init__(**kwargs)


class Graph_3(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_3, self).__init__(**kwargs)


class Graph_4(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_4, self).__init__(**kwargs)


class QuestionPopup(Popup):

    test_text = "Ilość modułów wyprodukowanych w APA."
    tc_text = "Ilość komór temperaturowych gdzie będą kondycjonowane moduły."
    tr_text = "Ilość Test Roomów w których będą odbywać się testy."
    wich_text = "Ilość komór Walk-in w których będą odbywać się testy."
    trunk_text = "Ilość transportów z APA na dzień."
    frq_text = "Częstotliwość dokładania modułów do TC przez technika wsparcia (ustaw 0 jeżeli moduły mają być dokłądane od razu). "

    message = ObjectProperty()
    test_text_py = ObjectProperty()

    def __init__(self, *args, **kwargs):

        # self.hints = [self.test_text, self.tc_text, self.tr_text, self.wich_text, self.trunk_text, self.frq_text]
        super(QuestionPopup, self).__init__(**kwargs)

    def popup_dissmis(self):
            return self.dismiss()

    def open(self, id):
        # TODO: wersja not perfect ale done, jak zostanie czasu to się to ogarnie
        # funkcja uruchamiane poprzez button "?" i wyświetlająca szczegółową informację o komórce
        print(type(id))
        print(id)
        # self.message.text = id
        super(QuestionPopup, self).open()
        # TODO: określić wyjście z popup'a poprzez klawisz Enter


class LtsBoxLayout(BoxLayout):
    """
    Główny wygląd programu, zawierają się w nim wszystkie widgety
    """

    main = ObjectProperty()
    graphs_screens_py = ObjectProperty()
    screen_text_py = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(LtsBoxLayout, self).__init__(**kwargs)
        self.questionpopup = QuestionPopup()
        self.main_param = ['test_qty', 'frq_check_in', 'tc_qty', 'tr_qty', 'wich_qty', 'trunks_qty', 'frq_check_in']
        self.event_param = ['transport_time', 'check_in_time', 'condi_time', 'deploy_time', 'anal_time']
        self.main_param_lts = []
        self.event_param_lts = []
        self.time_format = "min"
        self.screens = {
            "Wykres 1": "graph_1",
            "Wykres 2": "graph_2",
            "Wykres 3": "graph_3",
            "Wykres 4": "graph_4"
        }


    def start(self):
        """
        Funkcja uruchamiana poprzez przycisk "Start", pobiera parametry od użytkownika
        i zapisuje do odpowiednich list.
        :return: None
        """
        for i in self.main_param:
            param = eval("self.main.ids.{}.text".format(i))
            self.main_param_lts.append(int(param))
        for i in self.event_param:
            param = eval("self.main.ids.{}.text".format(i))
            self.event_param_lts.append(int(param))
        # print(type(self.main_param_lts[0]))
        # print(self.event_param_lts)

        # sim = LTS.Manage(self.main_param_lts[0],
        #                  self.main_param_lts[1],
        #                  self.main_param_lts[2],
        #                  self.main_param_lts[3],
        #                  self.main_param_lts[4],
        #                  self.main_param_lts[5],
        #                  self.main_param_lts[6],
        #                  self.event_param_lts,
        #                  self.time_format)
        # sim.sim_run()

    def change_screen(self, screen_name):
        print(screen_name, self.screens[screen_name])
        self.screen_text_py.text = screen_name
        self.graphs_screens_py.current = self.screens[screen_name]

    def time_format(self, value):
        if value == "Minuty":
            self.time_format = "min"
        elif value == "Godziny":

            self.time_format = "hrs"
        elif value == "Dni":
            self.time_format = "day"
        elif value == "Miesiące":
            self.time_format = "mnt"
        elif value == "Lata":
            self.time_format = "yer"

class LtsApp(App):
    """
    Main program
    """
    def __init__(self, *args, **kwargs):
        super(LtsApp, self).__init__(**kwargs)
        self.use_kivy_settings = True  # póki co na True, ale docelowo damy False
        Window.bind(on_keyboard=self.enter_dissmis)

    def enter_dissmis(self, window, key, *args):
        if key == 13:
            return QuestionPopup.popup_dissmis(self.root.questionpopup)

    def build(self):
        self.title = "Symulacja procesu COP"
        Window.maximize()
        # Config.set("input", "mouse", "mouse, disable_multitouch")
        # Window.clearcolor = get_color_from_hex("#757575")
        return LtsBoxLayout()



if __name__ == '__main__':
    LtsApp().run()