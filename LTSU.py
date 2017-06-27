import pandas as pd
import numpy as np
import random
import os

class Manage:

    def __init__(self):

        # tworzenie DFa
        self.simDF = None
        self.gen_DF()

        # czasy eventów
        self.real_time = 0
        self.time_of_delivery = 60
        self.time_of_check_in = 20
        self.time_of_conditioning = 240
        self.time_of_deployment = 20
        self.time_of_analysis = 20

        # listy testów i zasobów
        self.test_list = []
        self.rsc_list = []
        self.finished = []

        # tworzenie zasobów
        self.rsc_list.append(RSC('TrumnaAPA', None, None))
        self.rsc_list.append(RSC('StorageLAB', None, None))
        self.gen_RSC(4, 'TC', 8)
        self.gen_RSC(4, 'TR', 1)
        self.gen_RSC(4, 'AT', 1)
        # TODO: ustawienie temp TCków - może funkjce badającą rozkłąd temp i ust
        # TODO: komór względem temp występującj najdczęściej

        print([item.name for item in self.rsc_list])

        # testy
        self.project_list = list(range(1, 5+1))
        self.gen_tests(100, self.project_list)
        print([[test.name, test.group, test.project] for test in self.test_list])






    def sim_run(self):
        # logika
        simulation = True

        while simulation:
            for test in self.test_list:
                if test.ready_time == self.real_time:
                    self.event_run(test)
            self.real_time += 1
            if len(self.test_list) == len(self.finished):
                simulation = False
        print(self.simDF)
        return self.simDF

    def event_run(self, test):
        # TODO: od tyłu
        if test.status == 'New':
            #Delivery
            self.ev_delivery(test)
        elif test.status == 'Delivery':
            #Check_in
            self.ev_check_in(test)
        elif test.status == 'Check_in':
            #Conditioning
            self.ev_conditioning(test)
        elif test.status == 'Conditioning':
            #Deployment
            self.ev_deployment(test)
        elif test.status == 'Deployment':
            #Anlysis
            self.ev_analysis(test)
        elif test.status == 'Analysis':
            #Finito
            self.ev_finito(test)

    def ev_delivery(self, test):
        event_time = self.time_of_delivery
        test.set_status('Delivery')
        test.time_update(event_time)

        # ustalanie ilości trasportów na dzień i pbdługa trumie, kiedy ma być odpalany
        # jak ma pobierać z test lsty żeby nie dublowac tstów
        # pobierz real time
        # dodaj do df testy + ich detailsy + realtime

    def ev_check_in(self, test):
        event_time = self.time_of_check_in
        test.set_status('Check_in')
        test.set_temp()
        test.time_update(event_time)

        #pobierz i dodaj real_time

    def ev_conditioning(self, test):
        event_time = self.time_of_conditioning
        test.set_status('Conditioning')
        test.time_update(event_time)

        # TODO: jeżeli RT to event_time = 0
        # TODO: event conditioning musi spr wydajność TR
        # TODO: dodawanie skondycjonowanych modułów do rdy lst

    def ev_deployment(self, test):
        event_time = self.time_of_deployment
        test.set_status('Deployment')
        test.time_update(event_time)

        # pobierz i dodaj real_time

    def ev_analysis(self, test):
        event_time = self.time_of_analysis
        test.set_status('Analysis')
        test.time_update(event_time)

        # pobierz i dodaj real_time
        # TODO kolejka testów

    def ev_finito(self, test):
        test.set_status('Finished')
        self.finished.append(test)
        # pobierz i dodaj real_time, aktualizuj DF

    def gen_tests(self, qty, project):

        for i in range(qty):
            test_name = 'Test_{}'.format(i+1)
            self.test_list.append(Module(test_name, project))
        print('Dodano %d testów do \'test_list\'y' % (qty))
        return None

    def gen_RSC(self, qty, rsc_type, limit=None, temp=None):

        for i in range(qty):
            rsc_name = rsc_type + '_{}'.format(i+1)
            self.rsc_list.append(RSC(rsc_name, limit, temp))
        # print('Dodano zasoby %s_1 do %s_%d' % (rsc_type, rsc_type, qty))

    def gen_DF(self):

        # cols = ['Time_0', 'Delivery', 'Time_1', 'Check_in', 'Time_2',
        #         'Conditioning', 'Time_3', 'Deployment', 'Time_4', 'Analisys',
        #         'Time_5', 'Final', 'kind', 'project', 'temp', 'result']

        cols = ['Test_No', 'Time', 'Project', 'Group', 'Status', 'RSC', 'Result_eval']

        self.simDF = pd.DataFrame(columns=cols)

    def DF_update(self):
        pass

class RSC:

    def __init__(self, name, limit, temp):
        self.name = name
        self.limit  = limit
        self.temp = temp

        self.queue = []

        # TODO: każdy rsc musi mieć liste, jeżeli limit == None to znaczy ze brak limitu
        # TODO: odpalenie eventu robi spr czy jest miejsce w rsc - jeśli tak to:
        # TODO:     spr czy jest co brac i czy jest zgodność parametrów (np temp)

class Module:

    group_list = 'DAB, PAB, KAB, SAB, IC'.split()
    temp_list = [[-35, -30], [23], [60, 80, 85, 90]]
    proj_dict = {}
    proj_cache = {}

    def __init__(self, name, project_lst):

        self.name = name
        self.status = 'New'
        self.temp = ''
        self.project = ''
        self.group = random.choice(self.group_list)
        self.set_project(project_lst)
        self.set_temp()

        self.ready_time = ''
        self.result_eval = ''

    def set_status(self, status):
        self.status = status

    def set_temp(self):

        pos = self.get_proj_min_value_pos()
        temp = self.proj_dict[self.project][pos]
        self.temp = temp
        self.proj_cache[self.project][pos] += 1
        print(self.proj_cache)

    def set_project(self, project_lst):

        self.project = np.random.choice(project_lst)
        if not self.project in self.proj_dict:
            temps = []
            for i in range(3):
                if i == 0:
                    for j in range(int(np.random.choice([1, 2], 1, p=[.95, .05]))):
                        temps.append(int(np.random.choice(self.temp_list[i], 1, p=[0.7, 0.3])))
                elif i == 1:
                    for j in range(int(np.random.choice([1, 2], 1, p=[.95, .05]))):
                        temps.append(self.temp_list[i][0])
                elif i == 2:
                    for j in range(int(np.random.choice([1, 2], 1, p=[.95, .05]))):
                        temps.append(int(np.random.choice(self.temp_list[i], 1, p=[0.05, 0.25, 0.6, 0.1])))

            self.proj_dict[self.project] = temps
            self.proj_cache[self.project] = [0, 0, 0]

            print(self.proj_dict)

    def get_proj_min_value_pos(self):

        min_val = min(self.proj_cache[self.project])
        pos = self.proj_cache[self.project].index(min_val)

        return pos


    def time_update(self, event_time):
        self.ready_time += event_time


kupa = Manage()
kupa.sim_run()


