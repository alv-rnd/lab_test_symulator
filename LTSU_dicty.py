import pandas as pd
import numpy as np
import random
import os

class Manage:

    def __init__(self):

        # czasy eventów
        self.real_time = 0
        self.time_of_delivery = 60
        self.time_of_check_in = 20
        self.time_of_conditioning = 240
        self.TC_refill_time = 120
        self.time_of_deployment = 20
        self.time_of_analysis = 20

        # listy testów i zasobów
        self.test_list = []
        self.rsc_list = []
        self.finished = []

        # testy
        self.project_list = list(range(1, 5+1))
        self.gen_tests(100, self.project_list)

        # tworzenie zasobów
        # self.rsc_list.append(RSC('TrumnaAPA', 0, None, r_source='New'))
        # self.rsc_list.append(RSC('StorageLAB', 0, None, r_source='Delivery'))
        # self.rsc_list.append(RSC('TC_RT', 0, 23, r_source='Check_in'))
        # self.rsc_list.append(RSC('TC_1', 8, -35, r_source='Check_in'))
        # self.rsc_list.append(RSC('TC_2', 8, -30, r_source='Check_in'))
        # self.rsc_list.append(RSC('TC_3', 8, 60, r_source='Check_in'))
        # self.rsc_list.append(RSC('TC_4', 8, 80, r_source='Check_in'))
        # self.rsc_list.append(RSC('TC_5', 8, 85, r_source='Check_in'))
        # self.rsc_list.append(RSC('TC_6', 8, 90, r_source='Check_in'))
        # self.gen_RSC(4, 'TR', 1, r_source='Conditioning')
        # self.gen_RSC(4, 'AT', 1, r_source='Deployment', queue=True)

        # słowniki zasobów:
        self.delivery = {'TrumnaAPA': [0, 0]}
        self.check_in = {'StorageLAB': [0, 0]}
        self.conditioning = {'23': [0, 0],
                             '-35': [0, 8],
                             '-30': [0, 8],
                             '60': [0, 8],
                             '80': [0, 8],
                             '85': [0, 8],
                             '90': [0, 8]}
        self.deployment = {'TR_1': [0, 1],
                           'TR_2': [0, 1],
                           'TR_3': [0, 1],
                           'TR_4': [0, 1]}
        self.analysis = {'AT_1': [0, 1],
                         'AT_2': [0, 1],
                         'AT_3': [0, 1],
                         'AT_4': [0, 1]}

        # tempD = {}
        # for test in self.test_list:
        #     if not test.temp == 23:
        #         if str(test.temp) not in tempD.keys():
        #             tempD[str(test.temp)] = 1
        #         else:
        #             tempD[str(test.temp)] += 1
        #
        #
        # TC_qty = len(tempD.values())
        # for tc in self.rsc_list:
        #     if tc.r_source == 'Check_in':
        #         for temp in tempD.keys():
        #             tc.set_temp(int(temp))
        #
        # print([item.name for item in self.rsc_list])

        # tworzenie DFa
        self.simDF = None
        self.gen_DF()

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
        # od tyłu jest fajniej
        if test.status == 'Analysis':
            #Finito
            self.ev_finito(test)
        elif test.status == 'Deployment':
            #Anlysis
            self.ev_analysis(test)
        elif test.status == 'Conditioning':
            #Deployment
            self.ev_deployment(test)
        elif test.status == 'Check_in':
            # Conditioning
            self.ev_conditioning(test)
        elif test.status == 'Delivery':
            #Check_in
            self.ev_check_in(test)
        elif test.status == 'New':
            #Delivery
            self.ev_delivery(test)

    def ev_delivery(self, test):

        event_time = self.time_of_delivery
        status = 'Delivery'

        self.delivery['TrumnaAPA'][0] += 1

        test.set_location('TrumnaAPA')
        test.set_status(status)
        test.time_update(event_time)

        self.simDF.loc[test.name]['Time_0'] = self.real_time
        self.simDF.loc[test.name]['Group'] = test.group
        self.simDF.loc[test.name]['Project'] = test.project
        self.simDF.loc[test.name]['Temp'] = test.temp
        self.simDF.loc[test.name][status] = 'TrumnaAPA'

        # ustalanie ilości trasportów na dzień i pbdługa trumie, kiedy ma być odpalany
        # jak ma pobierać z test lsty żeby nie dublowac tstów
        # pobierz real time
        # dodaj do df testy + ich detailsy + realtime

    def ev_check_in(self, test):
        event_time = self.time_of_check_in
        status = 'Check_in'

        self.delivery[test.location][0] -= 1
        self.check_in['StorageLAB'][0] += 1

        test.set_location('StorageLAB')
        test.set_status(status)
        test.time_update(event_time)

        self.simDF.loc[test.name]['Time_1'] = self.real_time
        self.simDF.loc[test.name][status] = 'StorageLAB'

        print(self.check_in)
        print(self.delivery)
        # cols = ['Time_0', 'Delivery', 'Time_1', 'Check_in', 'Time_2',
        #         'Conditioning', 'Time_3', 'Deployment', 'Time_4', 'Analisys',
        #         'Time_5', 'Final', 'kind', 'project', 'temp', 'result']

    def ev_conditioning(self, test):
        event_time = (1 if test.temp == 23 else 240)
        status = 'Conditioning'
        TC_fill = self.TC_refill_time
        tr_count = len(self.deployment.keys())
        tc_test_sum = 0

        for key in self.conditioning.keys():
            tc_test_sum += self.conditioning[key][0]

        if tc_test_sum < int(tr_count * TC_fill / self.time_of_deployment):
            if self.conditioning[str(test.temp)][1] == 0:
                self.check_in[test.location][0] -= 1
                self.conditioning[str(test.temp)][0] += 1
                self.simDF.loc[test.name]['Time_2'] = self.real_time
                self.simDF.loc[test.name][status] = 'TC_{}'.format(test.temp)
                test.set_location(str(test.temp))
                test.set_status(status)
                test.time_update(event_time)
            else:
                limit = self.conditioning[str(test.temp)][1]
                if self.conditioning[str(test.temp)][0] < limit:
                    self.check_in[test.location][0] -= 1
                    self.conditioning[str(test.temp)][0] += 1
                    self.simDF.loc[test.name]['Time_2'] = self.real_time
                    self.simDF.loc[test.name][status] = 'TC_{}'.format(test.temp)
                    test.set_location(str(test.temp))
                    test.set_status(status)
                    test.time_update(event_time)
        print(self.check_in)
        print(self.conditioning)

    def ev_deployment(self, test):
        event_time = self.time_of_deployment
        status = 'Deployment'

        for tr in self.deployment.keys():
            if self.deployment[tr][0] == 0:

                self.deployment[tr][0] += 1
                self.conditioning[str(test.temp)][0] -= 1

                test.set_status(status)
                test.time_update(event_time)
                test.set_location(tr)

                self.simDF.loc[test.name]['Time_3'] = self.real_time
                self.simDF.loc[test.name][status] = tr
                break
        print(self.conditioning)
        print(self.deployment)

    def ev_analysis(self, test):
        event_time = self.time_of_analysis
        status = 'Analysis'

        for at in self.analysis.keys():
            if self.analysis[at][0] < self.analysis[at][1]:
                self.analysis[at][0] += 1
                self.deployment[test.location][0] -= 1
                # for tr in self.deployment.keys():
                #     if self.deployment[tr][0] == self.deployment[tr][1]:
                #         self.deployment[tr][0] -= 1
                #         break

                test.set_status(status)
                test.time_update(event_time)
                test.set_location(at)

                self.simDF.loc[test.name]['Time_4'] = self.real_time
                self.simDF.loc[test.name][status] = at
                self.simDF.loc[test.name]['Result'] = np.random.choice(['OK', 'COK', 'NOK'], 1,
                                                    p=[.85, .10, .05])
                break
        print(self.deployment)
        print(self.analysis)

    def ev_finito(self, test):
        status = 'Finished'
        self.analysis[test.location][0] -= 1

        test.set_status(status)
        self.finished.append(test)

        self.simDF.loc[test.name]['Time_5'] = self.real_time
        self.simDF.loc[test.name][status] = status

        # cols = ['Time_0', 'Delivery', 'Time_1', 'Check_in', 'Time_2',
        #         'Conditioning', 'Time_3', 'Deployment', 'Time_4', 'Analisys',
        #         'Time_5', 'Finished', 'kind', 'project', 'temp', 'result']

        print([(test.name, test.temp) for test in self.finished])

    def gen_tests(self, qty, project):

        for i in range(qty):
            test_name = 'Test_{}'.format(i+1)
            self.test_list.append(Module(test_name, project))
        print('Dodano %d testów do \'test_list\'y' % (qty))
        return None

    # def gen_RSC(self, qty, rsc_type, limit=0, temp=None, r_source=None, queue=False):
    #
    #     for i in range(qty):
    #         rsc_name = rsc_type + '_{}'.format(i+1)
    #         self.rsc_list.append(RSC(rsc_name, limit, temp, r_source, queue))
    #     # print('Dodano zasoby %s_1 do %s_%d' % (rsc_type, rsc_type, qty))

    def gen_DF(self):

        cols = ['Time_0', 'Delivery', 'Time_1', 'Check_in', 'Time_2',
                'Conditioning', 'Time_3', 'Deployment', 'Time_4', 'Analisys',
                'Time_5', 'Finished', 'Group', 'Project', 'Temp', 'Result']

        # cols = ['Test_No', 'Time', 'Project', 'Group', 'Status', 'RSC', 'Result_eval']

        self.simDF = pd.DataFrame(columns=cols, index=[test.name for test in self.test_list])

    def DF_update(self):
        pass

# class RSC:
#
#     def __init__(self, name, limit, temp, r_source, queue=False):
#         self.name = name
#         self.limit  = limit
#         self.temp = temp
#         self.r_source = r_source    # rodzaj rsc ale odnoszący się do
#                             # stsatusu testu z porpzedniej fazy, potrzebuje
#                             # tego zeby dodawać testy do do odp rsc
#         self.queue = queue
#         self.in_progress = []
#
#         if queue == True:
#             self.queue = []
#
#     def add_to_in_progress(self, test, rsc_lst):
#
#         def wypierdalaj():
#             for rsc in rsc_lst:
#                 if test in rsc.in_progress:
#                     rsc.in_progress.remove(test)
#
#         if self.limit == 0:
#             wypierdalaj()
#             self.in_progress.append(test)
#         elif len(self.in_progress) < self.limit:            # dodawanie do in progress bo limit pozwala
#             if self.queue == False:
#                 wypierdalaj()
#                 self.in_progress.append(test)               # brak kolejki, dodajemy nromalnie
#             else:
#                 wypierdalaj()
#                 self.queue.append(test)                     # kolejka jest, dorzucamy do kolejki
#                 self.in_progress.append(self.queue.pop(0))  # pobieramy z kolejki pierwszy z brzegu (FIFO)
#         else:
#             if self.queue !=False:
#                 wypierdalaj()                                   # nic nie rob bo limit nie pozwala
#                 self.queue.append(test)  # dodawanie do queue o ile jest lub
#
#
#
#
#
#     def set_temp(self, temp):
#         self.temp = temp

class Module:

    group_list = 'DAB PAB KAB SAB IC'.split()
    temp_list = [[-35, -30], [23], [60, 80, 85, 90]]
    proj_dict = {}
    proj_cache = {}

    def __init__(self, name, project_lst):

        self.name = name
        self.status = 'New'
        self.temp = ''
        self.project = ''
        self.location = None
        self.group = random.choice(self.group_list)
        self.set_project(project_lst)
        self.set_temp()

        self.ready_time = 0
        self.result_eval = ''

    def set_status(self, status):
        self.status = status

    def set_location(self, rsc):
        self.location = rsc

    def set_temp(self):

        pos = self.get_proj_min_value_pos()
        temp = self.proj_dict[self.project][pos]
        self.temp = temp
        self.proj_cache[self.project][pos] += 1

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


    def get_proj_min_value_pos(self):

        min_val = min(self.proj_cache[self.project])
        pos = self.proj_cache[self.project].index(min_val)

        return pos

    def check_rsc_parameter(self, rsc_list):

        for rsc in rsc_list:
            if self.status == rsc.r_source:
                if rsc.limit == 0 or rsc.limit > len(rsc.in_progress):
                    if self.status == 'Check_in':
                        if self.temp == rsc.temp:
                            return rsc
                    else:
                        return rsc
        return False

        # można tu póżniej dodać param level określający ilość parametrów,
        # jaką ma badać dla danego eventu funkcja, np 0 - tylko temp, 1, stage, potem wielkość itp itd

    def time_update(self, event_time):
        self.ready_time += event_time


sim = Manage()
sim.sim_run()


