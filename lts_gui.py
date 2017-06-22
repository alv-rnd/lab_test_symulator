# -*- coding: UTF-8 -*-

import kivy

import LTS

import numpy as np
import math
import pandas as pd

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Canvas
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty
# from kivy.utils import get_color_from_hex

from kivy.garden.graph import Graph, MeshLinePlot

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt



# class Graph_1_Screen(Screen):
#     pass


class Graph_1(Screen):

    def __init__(self, *args, **kwargs):
        super(Graph_1, self).__init__(**kwargs)

        def press(event):
            print('press released from test', event.x, event.y, event.button)

        def release(event):
            print('release released from test', event.x, event.y, event.button)

        def resize(event):
            print('resize from mpl ', event)

    fig = plt.figure()
    figure = fig
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    df = pd.read_csv('world_bank.csv')
    print(df.columns[4:])
    ax1.plot_date(df.columns[4:], df.iloc[0][4:], '-', label="Kasz")
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.grid(True)

    plt.xlabel('Year')
    plt.ylabel('Kasz')
    plt.title('Wykres kaszu dla Polski na przestrzeni lat')
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

    # plt.show()


class Graph_2_Screen(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_2_Screen, self).__init__(**kwargs)


class Graph_2(Graph):

    def __init__(self, *args, **kwargs):
        super(Graph_2, self).__init__(**kwargs)

        self.xlabel= 'Qty'
        self.ylabel= 'T'
        self.x_ticks_minor= 5
        self.x_ticks_major= 25
        self.y_ticks_major= 1
        self.y_grid_label= True
        self.x_grid_label= True
        self.padding= 5
        self.x_grid= True
        self.y_grid= True
        self.xmin= -0
        self.xmax= 100
        self.ymin= -1
        self.ymax= 1
        self.plot = MeshLinePlot(color=[1, 1, 1, 1])
        self.plot.points = [(x, math.sin(x / 10.)) for x in range(-0, 101)]
        self.add_plot(self.plot)


class Graph_3(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_3, self).__init__(**kwargs)


class Graph_4(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_4, self).__init__(**kwargs)


class QuestionPopup(Popup):

    question_dict = {
    'test_text': "Ilość modułów wyprodukowanych w APA.",
    'tc_text': "Ilość komór temperaturowych gdzie będą kondycjonowane moduły.",
    'tr_text': "Ilość Test Roomów w których będą odbywać się testy.",
    'wich_text': "Ilość komór Walk-in w których będą odbywać się testy.",
    'trunk_text': "Ilość transportów z APA na dzień.",
    'frq_text': "Częstotliwość dokładania modułów do TC przez technika wsparcia (ustaw 0 jeżeli moduły mają być dokłądane od razu). "
    }

    message = ObjectProperty()

    def __init__(self, *args, **kwargs):

        # self.hints = [self.test_text, self.tc_text, self.tr_text, self.wich_text, self.trunk_text, self.frq_text]
        super(QuestionPopup, self).__init__(**kwargs)

    def popup_dissmis(self):
            return self.dismiss()

    def open(self, text):
        # TODO: wersja not perfect ale done, jak zostanie czasu to się to ogarnie
        # funkcja uruchamiane poprzez button "?" i wyświetlająca szczegółową informację o komórce
        self.message.text = self.question_dict[text]
        popup = super(QuestionPopup, self)
        popup.open()

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
            "Wykres 2": "graph_2_screen",
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

        sim = LTS.Manage(self.main_param_lts[0],
                         self.main_param_lts[1],
                         self.main_param_lts[2],
                         self.main_param_lts[3],
                         self.main_param_lts[4],
                         self.main_param_lts[5],
                         self.main_param_lts[6],
                         self.event_param_lts,
                         self.time_format)
        sim.sim_run()
        #
        # log = sim.real_time.log
        # print(log)



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
        if key in [13, 32]:
            return QuestionPopup.popup_dissmis(self.root.questionpopup)

    def build(self):
        self.title = "Symulacja procesu COP"
        Window.maximize()
        # Config.set("input", "mouse", "mouse, disable_multitouch")
        # Window.clearcolor = get_color_from_hex("#757575")
        return LtsBoxLayout()



if __name__ == '__main__':
    LtsApp().run()