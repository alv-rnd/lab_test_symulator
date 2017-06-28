# -*- coding: UTF-8 -*-

import kivy

import LTSU

import numpy as np
import math
import pandas as pd
import os
import datetime

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

    def get_fc(self, log, time=None):

        width = 0.5

        # x = [1, 2, 3, 4, 5, 6]
        # y = [5, 2, 4, 7, 9, 4]
        # y2 = [0, 0, 3, 2, 3, 0]
        #
        # statusy = ['Delivery', 'Check in', 'Conditioning', 'Deployment', 'Analisys', 'Finish']

        x = [1, 2, 3, 4, 5, 6]
        statusy = ['Delivery', 'Check in', 'Conditioning', 'Deployment', 'Analisys', 'Finish']
        y = [log[1], log[2], log[3], log[4], log[5], log[6] / 10]

        fig = plt.figure(facecolor='none')
        ax = fig.add_subplot(111)
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
        plt.title('Symulacja {} - {} min ({} hrs)'.format(1, (0 if time == None else round(time, 0)), 0 if time == None else round(time / 60, 1)), color='white', fontsize=20)
        plt.legend()

        for react in b1:
            if react == b1[-1]:
                height = react.get_height()
                ax.text(react.get_x() + react.get_width() / 2., 1.05 * height, '%d' %
                        int(height*10), ha='center', va='bottom', color='white')
            else:
                height = react.get_height()
                ax.text(react.get_x() + react.get_width() / 2., 1.05 * height, '%d' %
                        int(height), ha='center', va='bottom', color='white')


        # height_6 = b1[-1].get_height()
        # ax.text(b1[-1].get_x() + b1[-1].get_width() / 2., 1.05 * height_6, '%d' %
        #         int(height_6 * 10), ha='center', va='bottom', color='white')

        # ani = FuncAnimation(fig, update, frames=120, bl)

        wid = FigureCanvas(fig)

        # fig.canvas.mpl_connect('figure_enter_event', enter_figure)
        # fig.canvas.mpl_connect('figure_leave_event', leave_figure)
        # fig.canvas.mpl_connect('axes_enter_event', enter_axes)
        # fig.canvas.mpl_connect('axes_leave_event', leave_axes)
        # fig.canvas.mpl_connect('button_press_event', press)
        # fig.canvas.mpl_connect('button_release_event', release)
        # fig.canvas.mpl_connect('key_press_event', keypress)
        # fig.canvas.mpl_connect('key_release_event', keyup)
        # fig.canvas.mpl_connect('motion_notify_event', motionnotify)
        # fig.canvas.mpl_connect('resize_event', resize)
        # fig.canvas.mpl_connect('scroll_event', scroll)
        # fig.canvas.mpl_connect('figure_enter_event', figure_enter)
        # fig.canvas.mpl_connect('figure_leave_event', figure_leave)
        # fig.canvas.mpl_connect('close_event', close)



        return wid

    def add_plot(self, log, real_time=None):
        self.clear_widgets()
        # wid = self.get_fc()
        self.add_widget(self.get_fc(log, real_time))
        # self.add_widget(self.get_nav(wid))

class Graph_2_Screen(Screen):
    # graph_2_screen_py = ObjectProperty()
    def __init__(self, *args, **kwargs):
        super(Graph_2_Screen, self).__init__(**kwargs)
        # self.log = log
        # self.real_time = real_time
        # Graph_2(self.log, self.real_time)


class Graph_2(Graph):

    def __init__(self, *args, **kwargs):
        super(Graph_2, self).__init__(**kwargs)

        # self.log = log
        # self.real_time = real_time
        self.xlabel= 'Qty'
        self.ylabel= 'T'
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
        self.plot = MeshLinePlot(color=[60, 90, 60, 1])
        # self.plot2 = MeshLinePlot(color=[180, 90, 60, 1])
        # self.plot3 = MeshLinePlot(color=[300, 90, 60, 1])
        # self.plot4 = MeshLinePlot(color=[16, 90, 50, 1])
        # self.plot5 = MeshLinePlot(color=[280, 90, 50, 1])
        # self.plot6 = MeshLinePlot(color=[90, 90, 60, 1])
        self.plot.points = [(x, math.sin(x / 10)) for x in range(-0, 101)]
        # self.plot2.points = [(x, self.log[2]) for x in range(-0, self.real_time)]
        # self.plot3.points = [(x, self.log[3]) for x in range(-0, self.real_time)]
        # self.plot4.points = [(x, self.log[4]) for x in range(-0, self.real_time)]
        # self.plot5.points = [(x, self.log[5]) for x in range(-0, self.real_time)]
        # self.plot6.points = [(x, self.log[6]) for x in range(-0, self.real_time)]
        self.add_plot(self.plot)
        # self.add_plot(self.plot2)
        # self.add_plot(self.plot3)
        # self.add_plot(self.plot4)
        # self.add_plot(self.plot5)
        # self.add_plot(self.plot6)



class Graph_3(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_3, self).__init__(**kwargs)


class Graph_4(Screen):
    def __init__(self, *args, **kwargs):
        super(Graph_4, self).__init__(**kwargs)


class ExcelPopup(Popup):
    def __init__(self, *args, **kwargs):
        super(ExcelPopup, self).__init__(**kwargs)

    def export_show(self):
        super(ExcelPopup, self).open()

    def save(self, path, filename):
        pass

    # def popup_dissmis(self):
    #         return self.dismiss()

class QuestionPopup(Popup):

    question_dict = {
    'test_text': "Ilość modułów wyprodukowanych w APA.",
    'project_text': "Ilość możliwych do wygenerowania projektów.",
    'tc_cap_text': "Pojemność komór do kondycjonowania modułów.",
    'tr_text': "Ilość pomieszczeń testowych.",
    'trunk_text': "Pojemność tumny.",
    'at_qty_text': "Ilosć stołów do analizy.",
    'tc_refill_time_text': "Częstość wrzutów do komr kondycjonujących.",
    'transport_text': "Czas transportu modułów z APA do Lab.",
    'check_in_text': "Czas przyjmowania modułów.",
    'conditioning_time_text': "Czas kondycjonowania modułów.",
    'deployment_time_text': "Czas trwania testu jednego modułu.",
    'analysis_time_text': "Czas trwania analizy jednego modułu."
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
    # graph_2_screen_py = ObjectProperty()
    graphs = []

    def __init__(self, *args, **kwargs):
        super(LtsBoxLayout, self).__init__(**kwargs)
        self.questionpopup = QuestionPopup()
        self.export = ExcelPopup()
        self.real_time = 100
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
        self.slid = 0
        self.log = None
        # self.graph_1_py =



    @staticmethod
    def prepare_log(log, slider=None):
        test_qty = 0 #len(log['Delivery']) #len(log)

        # slider = 400

        #delivery = log['Delivery'][log['Time_0'] < slider][log['Time_1'] > slider]
        delivery = len(log['Delivery'][log['Time_0'] < slider][log['Time_1'] > slider])

        # check_in = log['Check_in'][log['Time_1'] < slider][log['Time_2'] > slider]
        check_in = len(log['Check_in'][log['Time_1'] < slider][log['Time_2'] > slider])

        # conditioning = log['Conditioning'][log['Time_2'] < slider][log['Time_3'] > slider]
        conditioning = len(log['Conditioning'][log['Time_2'] < slider][log['Time_3'] > slider])

        # deployment = log['Deployment'][log['Time_3'] < slider][log['Time_4'] > slider]
        deployment = len(log['Deployment'][log['Time_3'] < slider][log['Time_4'] > slider])

        # analysis = log['Analysis'][log['Time_4'] < slider][log['Time_5'] > slider]
        analysis = len(log['Analysis'][log['Time_4'] < slider][log['Time_5'] > slider])

        # finished = log['Finished'][log['Time_5'] < slider]
        finished = len(log['Finished'][log['Time_5'] < slider])

        return [test_qty, delivery, check_in, conditioning, deployment, analysis, finished]

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

        sim1 = sim.sim_run()
        self.log = sim1[0]
        self.real_time = sim1[1]


        path_to_export = 'C:\\Users\mateusz.sobek\Desktop\Logi_sim_run\log_{}.xlsx'.format(np.random.random_integers(1000))

        self.log.to_excel(path_to_export)
        # if len(self.graphs) < 4:
        #     self.graphs.append(g)
        # else:
        #     # TODO: popup czy nadpisać pierwszy wykres
        #     self.graphs.pop(self.graphs[0])
        #     self.graphs.append(g)
        # print(self.prepare_log(log))
        self.graph_1_py.add_plot(self.prepare_log(self.log))
        # Graph_2(self.prepare_log(self.log), self.real_time)

    def export_excel(self):
        pass

    def slider_magic(self, instance, value):

        self.slid = value * self.real_time / 100

    def refresh(self):
        # self.graph_1_py.remove_plot()
        if self.log is None:
            pass
        else:
            self.graph_1_py.add_plot(self.prepare_log(self.log, self.slid), self.slid)

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
    def refresh_key(self, window, key, *args):
        if key in [9]:
            return self.root.refresh(self.root.refresh)

    def build(self):
        self.title = "Symulacja procesu COP"
        Window.maximize()
        # Config.set("input", "mouse", "mouse, disable_multitouch")
        # Window.clearcolor = get_color_from_hex("#757575")
        return LtsBoxLayout()



if __name__ == '__main__':
    LtsApp().run()