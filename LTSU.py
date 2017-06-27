import pandas as pd
import numpy as np
import random
import os



class Manage:

    def __init__(self):
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
        self.project_qty = 5
        self.test_qty = 100
        self.tr_qty = 4
        # self.wich_qty = wich_qty
        self.at_qty = 4
        self.trunk_qty = 50
        self.tc_cap = 8

        # testy
        self.project_list = list(range(1, self.project_qty + 1))
        self.gen_tests(self.test_qty, self.project_list)

        # tempD = {}
        # for test in self.test_list:
        #     if test.temp != 23:
        #         if str(test.temp) not in tempD.keys() and test.temp != 23:
        #             tempD[str(test.temp)] = 1
        #         else:
        #             tempD[str(test.temp)] += 1


        # TC_qty = len(tempD.values())
        # tworzenie zasobów
        self.rsc_list.append(RSC('TrumnaAPA', self.trunk_qty, None, r_source='New'))
        self.rsc_list.append(RSC('StorageLAB', 0, None, r_source='Delivery'))
        self.rsc_list.append([RSC('TC_RT', 0, 23, r_source='Check_in'), RSC('TC_1', self.tc_cap, -35, r_source='Check_in'),
                              RSC('TC_2', self.tc_cap, -30, r_source='Check_in'), RSC('TC_3', self.tc_cap, 60, r_source='Check_in'),
                              RSC('TC_4', self.tc_cap, 80, r_source='Check_in'), RSC('TC_5', self.tc_cap, 85, r_source='Check_in'),
                              RSC('TC_6', self.tc_cap, 90, r_source='Check_in')])
        self.gen_RSC(self.tr_qty, 'TR', 1)
        self.gen_RSC(self.at_qty, 'AT', 1)
        self.rsc_list[3].insert(self.tr_qty + 1, RSC('WICH_1', 1, None,r_source='Conditioning', inout='IN'))
        self.rsc_list[3].insert(self.tr_qty + 2, RSC('WICH_2', 1, None,r_source='Conditioning', inout='IN'))

        # print([rsc for rsc in self.rsc_list])
        # #
        # print([rsc.name for rsc in self.rsc_list[2]])
        # print([rsc.name for rsc in self.rsc_list[3]])
        # print([rsc.name for rsc in self.rsc_list[4]])

        # TODO: ustawienie temp TCków - może funkjce badającą rozkłąd temp i ust
        # TODO: komór względem temp występującj najdczęściej

        # tworzenie DFa
        self.simDF = None
        self.gen_DF()

    def sim_run(self):
        # logika
        simulation = True

        while simulation:
            for test in self.test_list:
                if test.ready_time == self.real_time:
                    prev_time = test.ready_time
                    self.event_run(test)
                    if prev_time == test.ready_time:
                        test.ready_time += 1
            self.real_time += 1
            # print(self.real_time)
            # if self.real_time == 1000:
            #     print([test.name for test in self.rsc_list[1].in_progress])
            #     break
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
        elif test.status == 'New' and (self.real_time == 0 or self.real_time % 480 == 0):
            #Delivery
            self.ev_delivery(test)

    # def event_run(self, test):
    #     # od przodu też jest nieźle
    #     if test.status == 'New' and (self.real_time == 0 or self.real_time % 480 == 0):
    #         #Delivery
    #         self.ev_delivery(test)
    #     elif test.status == 'Delivery':
    #         #Check_in
    #         self.ev_check_in(test)
    #     elif test.status == 'Check_in':
    #         # Conditioning
    #         self.ev_conditioning(test)
    #     elif test.status == 'Conditioning':
    #         # Deployment
    #         self.ev_deployment(test)
    #     elif test.status == 'Deployment':
    #         #Anlysis
    #         self.ev_analysis(test)
    #     elif test.status == 'Analysis':
    #         #Finito
    #         self.ev_finito(test)

    def ev_delivery(self, test):

        event_time = self.time_of_delivery
        status = 'Delivery'

        rsc = self.rsc_list[0]
        if rsc:
            if rsc.limit > len(rsc.in_progress):
                rsc.in_progress.append(test)
                test.set_status(status)
                # test.set_location(rsc)
                test.time_update(event_time)

            self.simDF.loc[test.name]['Time_0'] = self.real_time
            self.simDF.loc[test.name]['Group'] = test.group
            self.simDF.loc[test.name]['Project'] = test.project
            self.simDF.loc[test.name]['Temp'] = test.temp
            self.simDF.loc[test.name][status] = rsc.name

        # ustalanie ilości trasportów na dzień i pbdługa trumie, kiedy ma być odpalany
        # jak ma pobierać z test lsty żeby nie dublowac tstów
        # pobierz real time
        # dodaj do df testy + ich detailsy + realtime

    def ev_check_in(self, test):
        event_time = self.time_of_check_in
        status = 'Check_in'

        prev_rsc_prog = self.rsc_list[0].in_progress

        rsc = self.rsc_list[1]
        if rsc:
            if test in prev_rsc_prog:
                prev_rsc_prog.remove(test)
            rsc.in_progress.append(test)
            test.set_status(status)
            # test.set_location(rsc)
            test.time_update(event_time)

            self.simDF.loc[test.name]['Time_1'] = self.real_time
            self.simDF.loc[test.name][status] = rsc.name

        # cols = ['Time_0', 'Delivery', 'Time_1', 'Check_in', 'Time_2',
        #         'Conditioning', 'Time_3', 'Deployment', 'Time_4', 'Analisys',
        #         'Time_5', 'Final', 'kind', 'project', 'temp', 'result']

    def ev_conditioning(self, test):
        if test.temp == 23:
            event_time = 1
        else:
            event_time = self.time_of_conditioning

        status = 'Conditioning'
        TC_fill = self.TC_refill_time
        test_sum = 0
        tr_count = len(self.rsc_list[3])

        for tc in self.rsc_list[2]:    # koreślenie sumy testów w komorach
            test_sum += len(tc.in_progress)

        prev_rsc_prog = self.rsc_list[1].in_progress

        rsc = test.check_rsc_parameter_cond(self.rsc_list[2])
        # print('rsc temp', rsc.temp, 'test temp', test.temp)
        if test_sum < int(tr_count * TC_fill / self.time_of_deployment):
            if rsc:
                rsc.in_progress.append(test)
                test.set_status(status)
                # test.set_location(rsc)
                test.time_update(event_time)

                self.simDF.loc[test.name]['Time_2'] = self.real_time
                self.simDF.loc[test.name][status] = rsc.name
        if test in prev_rsc_prog:
            prev_rsc_prog.remove(test)

    def ev_deployment(self, test):


        event_time =(self.time_of_deployment if test.inout == 'OUT' else self.time_of_deployment + 30)
        status = 'Deployment'

        prev_rsc_list = self.rsc_list[2]

        rsc = test.check_rsc_parameter_deploy(self.rsc_list[3])
        if rsc:
            rsc.in_progress.append(test)
            test.set_status(status)
            # test.set_location(rsc)
            test.time_update(event_time)

            self.simDF.loc[test.name]['Time_3'] = round(self.real_time, -1)
            self.simDF.loc[test.name][status] = rsc.name
        for rsc in prev_rsc_list:
            if test in rsc.in_progress:
                rsc.in_progress.remove(test)

    def ev_analysis(self, test):
        event_time = self.time_of_analysis
        status = 'Analysis'

        prev_rsc_list = self.rsc_list[3]

        rsc = test.check_rsc_parameter_anal(self.rsc_list[4])
        if rsc:
            rsc.in_progress.append(test)
            test.set_status(status)
            # test.set_location(rsc)
            test.time_update(event_time)

            self.simDF.loc[test.name]['Time_4'] = self.real_time
            self.simDF.loc[test.name][status] = rsc.name
            self.simDF.loc[test.name]['Result'] = np.random.choice(['OK', 'COK', 'NOK'], 1,
                                                    p=[.85, .10, .05])
        for rsc in prev_rsc_list:
            if test in rsc.in_progress:
                rsc.in_progress.remove(test)

    def ev_finito(self, test):
        status = 'Finished'
        prev_rsc_list = self.rsc_list[4]
        test.set_status(status)
        # test.set_location(status)

        self.simDF.loc[test.name]['Time_5'] = self.real_time
        self.simDF.loc[test.name][status] = status

        self.finished.append(test)
        for rsc in prev_rsc_list:
            if test in rsc.in_progress:
                rsc.in_progress.remove(test)
        # cols = ['Time_0', 'Delivery', 'Time_1', 'Check_in', 'Time_2',
        #         'Conditioning', 'Time_3', 'Deployment', 'Time_4', 'Analisys',
        #         'Time_5', 'Finished', 'kind', 'project', 'temp', 'result']

    def gen_tests(self, qty, project):

        for i in range(qty):
            test_name = 'Test_{}'.format(i+1)
            self.test_list.append(Module(test_name, project))
        print('Dodano %d testów do \'test_list\'y' % (qty))
        return None

    def gen_RSC(self, qty, rsc_type, limit):

        if rsc_type == 'TR':
            self.rsc_list.insert(3, [])
            for i in range(qty):
                rsc_name = rsc_type + '_{}'.format(i+1)
                self.rsc_list[3].append(RSC(rsc_name, limit, None, r_source='Conditioning'))
        elif rsc_type == 'AT':
            self.rsc_list.insert(4, [])
            for i in range(qty):
                rsc_name = rsc_type + '_{}'.format(i + 1)
                self.rsc_list[4].append(RSC(rsc_name, limit, None, r_source='Deployment'))

    def gen_DF(self):

        cols = ['Time_0', 'Delivery', 'Time_1', 'Check_in', 'Time_2',
                'Conditioning', 'Time_3', 'Deployment', 'Time_4', 'Analysis',
                'Time_5', 'Finished', 'Group', 'Project', 'Temp', 'Result']

        # cols = ['Test_No', 'Time', 'Project', 'Group', 'Status', 'RSC', 'Result_eval']

        self.simDF = pd.DataFrame(columns=cols, index=[test.name for test in self.test_list])

    def DF_update(self):
        pass

class RSC:

    def __init__(self, name, limit, temp, r_source, queue=False, inout='OUT'):
        self.name = name
        self.limit  = limit
        self.temp = temp
        self.r_source = r_source    # rodzaj rsc ale odnoszący się do
                            # stsatusu testu z porpzedniej fazy, potrzebuje
                            # tego zeby dodawać testy do do odp rsc
        self.queue = queue
        self.inout = inout
        self.in_progress = []

        if queue == True:
            self.queue = []

    def add_to_in_progress(self, test):
        if self.limit == 0:
            self.in_progress.append(test)
        elif len(self.in_progress) < self.limit:            # dodawanie do in progress bo limit pozwala
            if self.queue == False:
                self.in_progress.append(test)               # brak kolejki, dodajemy nromalnie
            else:
                self.queue.append(test)                     # kolejka jest, dorzucamy do kolejki
                self.in_progress.append(self.queue.pop(0))  # pobieramy z kolejki pierwszy z brzegu (FIFO)
        else:
            if self.queue !=False: self.queue.append(test)  # dodawanie do queue o ile jest lub
                                                            # nic nie rob bo limit nie pozwala

    def set_temp(self, temp):
        self.temp = temp

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
        self.inout = 'OUT'
        self.group = random.choice(self.group_list)
        self.set_project(project_lst)
        self.set_temp()

        self.ready_time = 0
        self.result_eval = ''

    def set_status(self, status):
        self.status = status

    # def set_location(self, rsc):
    #     if not self.location == None:
    #         self.location.in_progress.remove(self)
    #     self.location = rsc

    def set_temp(self):

        pos = self.get_proj_min_value_pos()
        temp = self.proj_dict[self.project][pos]
        self.temp = temp
        if self.temp != 23:
            self.inout = self.proj_dict[self.project][-1]
        self.proj_cache[self.project][pos] += 1

    def set_project(self, project_lst):

        self.project = np.random.choice(project_lst)
        if not self.project in self.proj_dict:
            temps = []
            for i in range(4):
                if i == 0:
                    for j in range(int(np.random.choice([1, 2], 1, p=[.95, .05]))):
                        temps.append(int(np.random.choice(self.temp_list[i], 1, p=[0.7, 0.3])))
                elif i == 1:
                    for j in range(int(np.random.choice([1, 2], 1, p=[.95, .05]))):
                        temps.append(self.temp_list[i][0])
                elif i == 2:
                    for j in range(int(np.random.choice([1, 2], 1, p=[.95, .05]))):
                        temps.append(int(np.random.choice(self.temp_list[i], 1, p=[0.05, 0.25, 0.6, 0.1])))
                elif i ==3:
                    temps.append(np.random.choice(['IN', 'OUT'], 1, p=[0.25, 0.75]))

            self.proj_dict[self.project] = temps
            self.proj_cache[self.project] = [0, 0, 0]


    def get_proj_min_value_pos(self):

        min_val = min(self.proj_cache[self.project])
        pos = self.proj_cache[self.project].index(min_val)

        return pos

    def check_rsc_parameter_cond(self, rsc_list):

        for rsc in rsc_list:
            if self.temp == 23 and rsc.limit == 0:
                return rsc
            elif rsc.limit > len(rsc.in_progress):
                if rsc.temp == self.temp:
                    return rsc

    def check_rsc_parameter_deploy(self, rsc_list):

        for rsc in rsc_list:
            if len(rsc.in_progress) == 0:
                if rsc.inout == 'IN' and self.inout == 'IN':
                    return rsc
                elif rsc.inout == 'OUT' and self.inout == 'OUT':
                    return rsc
                # return rsc

    def check_rsc_parameter_anal(self, rsc_list):

        for rsc in rsc_list:
            if len(rsc.in_progress) == 0:
                return rsc

    # def check_rsc_parameter_Cond(self, rsc_list):
    #     tc_lst = []
    #     for rsc in rsc_list:
    #         if rsc.r_source == 'Check_in':
    #             tc_lst.append(rsc)
    #     print([tc.name for tc in tc_lst])
    #     for rsc in tc_lst:
    #         if self.temp == rsc.temp:
    #             return rsc



        # można tu póżniej dodać param level określający ilość parametrów,
        # jaką ma badać dla danego eventu funkcja, np 0 - tylko temp, 1, stage, potem wielkość itp itd

    def time_update(self, event_time):
        self.ready_time += event_time


sim = Manage()
sim.sim_run()


