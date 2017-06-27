# -*- coding: UTF-8 -*-

import kivy

import LTSU

import numpy as np
import math
import pandas as pd
import os

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Canvas
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.properties import ObjectProperty, NumericProperty
# from kivy.utils import get_color_from_hex

from kivy.garden.graph import Graph, MeshLinePlot

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas, NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.figure as Figure
from matplotlib.animation import FuncAnimation



def enter_axes(event):
    print('enter_axes', event.inaxes)
    event.inaxes.patch.set_facecolor('yellow')
    event.canvas.draw()

def leave_axes(event):
    print('leave_axes', event.inaxes)
    event.inaxes.patch.set_facecolor('white')
    event.canvas.draw()

def enter_figure(event):
    print('enter_figure', event.canvas.figure)
    event.canvas.figure.patch.set_facecolor('red')
    event.canvas.draw()

def leave_figure(event):
    print('leave_figure', event.canvas.figure)
    event.canvas.figure.patch.set_facecolor('grey')
    event.canvas.draw()

def press(event):
    print('press released from test', event.x, event.y, event.button)


def release(event):
    print('release released from test', event.x, event.y, event.button)


def keypress(event):
    print('key down', event.key)


def keyup(event):
    print('key up', event.key)


def motionnotify(event):
    print('mouse move to ', event.x, event.y)


def resize(event):
    print('resize from mpl ', event.width, event.height)


def scroll(event):
    print('scroll event from mpl ', event.x, event.y, event.step)


def figure_enter(event):
    print('figure enter mpl')


def figure_leave(event):
    print('figure leaving mpl')


def close(event):
    print('closing figure')


class Graph_1(Screen):



    def __init__(self, *args, **kwargs):
        super(Graph_1, self).__init__(**kwargs)


    def get_nav(self, wid):
        nav = NavigationToolbar(wid)
        return nav.actionbar

    def get_fc(self, log):

        width = 0.5

        # x = [1, 2, 3, 4, 5, 6]
        # y = [5, 2, 4, 7, 9, 4]
        # y2 = [0, 0, 3, 2, 3, 0]
        #
        # statusy = ['Delivery', 'Check in', 'Conditioning', 'Deployment', 'Analisys', 'Finish']

        x = [1, 2, 3]
        statusy = ['Delivery', 'Check in', 'Conditioning']
        y = [log[0], log[0], log[0]]

        fig = plt.figure(facecolor='none')
        ax = fig.add_subplot(111, animated=True)
        ax.set_facecolor('none')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('none')

        xa = ax.xaxis
        ya = ax.yaxis

        xa.set_tick_params(labelcolor='white')
        xa.set_tick_params(color='white')
        ya.set_tick_params(labelcolor='white')
        ya.set_tick_params(color='white')

        b1 = plt.bar(x, y, width=width)
        # b2 = plt.bar(x, y2, color='red', bottom=y, width=width)

        plt.xticks(x, statusy)
        plt.xlabel('Statusy testów', color='white', fontsize=16)
        plt.ylabel('Ilość testów', color='white', fontsize=16)
        plt.title('Symulacja {}'.format(1), color='white', fontsize=20)
        plt.legend()

        # ani = FuncAnimation(fig, update, frames=120, bl)

        wid = FigureCanvas(fig)

        # fig.canvas.mpl_connect('figure_enter_event', enter_figure)
        # fig.canvas.mpl_connect('figure_leave_event', leave_figure)
        # fig.canvas.mpl_connect('axes_enter_event', enter_axes)
        # fig.canvas.mpl_connect('axes_leave_event', leave_axes)
        fig.canvas.mpl_connect('button_press_event', press)
        fig.canvas.mpl_connect('button_release_event', release)
        fig.canvas.mpl_connect('key_press_event', keypress)
        fig.canvas.mpl_connect('key_release_event', keyup)
        fig.canvas.mpl_connect('motion_notify_event', motionnotify)
        fig.canvas.mpl_connect('resize_event', resize)
        fig.canvas.mpl_connect('scroll_event', scroll)
        fig.canvas.mpl_connect('figure_enter_event', figure_enter)
        fig.canvas.mpl_connect('figure_leave_event', figure_leave)
        fig.canvas.mpl_connect('close_event', close)



        return wid

    def add_plot(self, log):

        # wid = self.get_fc()
        self.add_widget(self.get_fc(log))
        # self.add_widget(self.get_nav(wid))


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


# class TimeSlider(Slider):
#     time_slider_py = ObjectProperty()
#
#     self.



class LtsBoxLayout(BoxLayout):
    """
    Główny wygląd programu, zawierają się w nim wszystkie widgety
    """

    main = ObjectProperty()
    graph_1_py = ObjectProperty()
    time_slider_1_py = ObjectProperty()
    # screen_text_py = ObjectProperty()
    graphs = []

    def __init__(self, *args, **kwargs):
        super(LtsBoxLayout, self).__init__(**kwargs)
        self.questionpopup = QuestionPopup()
        self.main_param = ['test_qty',
                 'project_qty',
                 'tc_cap',
                 'tr_qty',
                 'trunk_cap',
                 'delivery_time',
                 'check_in_time',
                 'conditioning_time',
                 'tc_refill_time',
                 'deployment_time',
                 'analysis_time',
                 'at_qty']

        self.main_param_lts = []
        self.event_param_lts = []
        self.time_format = "min"
        self.screens = {
            "Symulacja 1": "graph_1",
            "Symulacja 2": "graph_2_screen",
            "Symulacja 3": "graph_3",
            "Symulacja 4": "graph_4"
        }

    @staticmethod
    def prepare_log(log):
        test_qty = len(log)
        # loq = log.iloc[:, 2:6]
        time1 = log['Time_1']
        delivery = log['Delivery']
        time2 = log['Time_2']
        check_in = log['Check_in']
        time3 = log['Time_3']
        condi = log['Conditioning']

        return [test_qty, time1, delivery, time2, check_in, time3, condi]


    def start(self):
        """
        Funkcja uruchamiana poprzez przycisk "Start", pobiera parametry od użytkownika
        i zapisuje do odpowiednich list.
        :return: None
        """

        for i in self.main_param:
            param = eval("self.main.ids.{}.text".format(i))
            self.main_param_lts.append(int(param))
        # for i in self.event_param:
        #     param = eval("self.main.ids.{}.text".format(i))
        #     self.event_param_lts.append(int(param))

        sim = LTSU.Manage(self.main_param_lts[0],
                          self.main_param_lts[1],
                          self.main_param_lts[2],
                          self.main_param_lts[3],
                          self.main_param_lts[4],
                          self.main_param_lts[5],
                          self.main_param_lts[6],
                          self.main_param_lts[7],
                          self.main_param_lts[8],
                          self.main_param_lts[9],
                          self.main_param_lts[10],
                          self.main_param_lts[11])
        # sim.sim_run()



        # if len(self.graphs) < 4:
        #     self.graphs.append(g)
        # else:
        #     # TODO: popup czy nadpisać pierwszy wykres
        #     self.graphs.pop(self.graphs[0])
        #     self.graphs.append(g)

        self.graph_1_py.add_plot(self.prepare_log(sim.sim_run()))

    def slider_magic(self, instance, value):
        print(int(value))


    def change_screen(self, screen_name):
        print(screen_name, self.screens[screen_name])
        self.screen_text_py.text = screen_name
        self.graphs_screens_py.current = self.screens[screen_name]

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