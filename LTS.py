# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import random
import os


class Manage:
    more = True
    '''
    Klasa zarządzająca wszytkim
    '''
    def __init__(self, t_qty, tc_qty, tc_cap, tr_qty, at_qty, frq_check_in, all_day, event_param_lts, time_format):
        self.t_qty = t_qty
        self.tc_qty = tc_qty
        self.tc_cap = tc_cap
        self.tr_qty = tr_qty
        self.at_qty = at_qty
        self.frq_check_in = frq_check_in
        self.all_day = all_day
        self.time_format = time_format
        self.test_list = []
        self.other_RSC =[]
        self.TC_list = []
        self.TR_list = []
        self.AT_list = []
        self.ready_list = []
        self.gen_ALL_RSCs(self.t_qty, self.tc_qty, self.tc_cap, self.tr_qty, self.at_qty)
        self.event_time = event_param_lts
        self.real_time = Time(self.test_list, self.time_format)


    @staticmethod # chciałem zobaczyć czy się uda to zrobić w tym, może być na około
    def transport_qty(transport_qty, approach=True):
        """
        Normalnie transporty są tylko w ciągu dnia czyli 12 godzin, ale kto wie co przyniesie przyszłość :D
        :param transport_qty: ilośc transportów
        :param approach: domyślnie 12 godzin, bo tak mamy ale zawsze można przyjąć 24h (checkbox w Kivy)
        :return: ilość transportów
        """
        if approach == True:
            day_time = 720
        else:
            day_time = 1440
        q = day_time / transport_qty
        return q

    def sim_run(self):

        test_qty = len(self.test_list)

        # TODO: kiedy ma być przerwanie whila? na razie dałem param 'more' który może być zmieniony jak ilość wygenerowanych testów będzie równa ilości testów w Fin
        while self.more:
            check_time = self.real_time.check_time()
            print(check_time)
            # Uruchomienie Eventów: Transport i Check-in jeżeli czas jest równy 0 lub jeżeli czas jest
            # podzielny przez wartość która zwraca 'transport_qty'
            if check_time == 0 or check_time % Manage.transport_qty(3, approach=self.all_day) == 0:
                Transport(self.test_list, self.other_RSC[0], self.event_time[0]).run_event()
                print('Transport')
                self.spotX_on_RSC_loaded(10, self.other_RSC[0])
                Check_in(self.other_RSC[0], self.other_RSC[1], self.event_time[1]).run_event()
                print('Check_in')
                self.spotX_on_RSC_loaded(10, self.other_RSC[1])

            # Uruchamianie Eventu Conditioning, musi być najpierw sprawdzenie czy frq_check_in jest równy 0,
            # inaczej wywala bład o dzieleniu przez 0 jeżeli od razu sprawdzimy modulo.
            if self.frq_check_in == 0:
                Conditioning(self.other_RSC[1], self.TC_list, self.event_time[2]).run_event()
                print('Conditioning')
                for TC in self.TC_list:
                    self.spotX_on_RSC_loaded(10, TC)

                #print('condi i frq_check == 0')
            elif check_time % self.real_time.time_converter(self.frq_check_in) == 0:
                Conditioning(self.other_RSC[1], self.TC_list, self.event_time[2]).run_event()
                print('Conditioning')
                for TC in self.TC_list:
                    self.spotX_on_RSC_loaded(10, TC)
                #print('condi i frq_check == 2')

            # Uruchomienie eventu Analiza, który "robi miejsca" w test roomach
            Analysis(self.TR_list, self.AT_list, self.event_time[4]).run_event(check_time)
            print('Alaliza')
            for AT in self.AT_list:
                self.spotX_on_RSC_loaded(1, AT)
            # Uruchomienie eventu Deployment
            Deployment(self.TC_list, self.TR_list, self.event_time[3]).run_event()
            print('TR')
            for TR in self.TR_list:
                self.spotX_on_RSC_loaded(1, TR)

            # Sprawdzenie czy ilość testów podana na początku jest równa ilości testów w kolejce Fin
            if test_qty == len(RSC_Analysis.finit) and test_qty != 0:
                print(RSC_Analysis.finit)
                self.more = False
            # albo jezeli czas jest równy czasowi podanemu przez użytkownika (wtedy test_qty == 0)
            # na razie to dla mnie żeby nie czekać całej kolejki testów
            elif check_time == 100:
                break

            # Zmieniłem na uruchamianie metody klasy Time, zamiast podbijania jej parametru,
            # wychodząc z tej zasady że jedna klasa nie wpływa na paramy innej klasy bezpośrednio
            self.real_time.add_real_time(1)



        # tmin = 0 #jakiś przykładowy czas w min
        # transport_qty_per_day = 3 #zgadnij
        # m = 24/transport_qty_per_day #do modulo w ifie ponizej
        #
        # trumnaAPA = self.other_RSC[0] # porawić couner gdyby zmienić kolejność tworzeni instancji w gen
        # storageLAB = self.other_RSC[1] # to też
        #
        # while True:
        #     if tmin == 0 or tmin%m == 0:
        #         self.gen_Tests(self.t_qty)
        #         Transport(self.test_list, trumnaAPA, 60) # a rozładunek?
        #         Check_in(trumnaAPA, storageLAB, 20)
        #     if tmin%120 == 0: # co 2h wrzucamy do kondycjonowania
        #         Conditioning(storageLAB, self.TC_list, 240, first_run=False(by default))
        #           for tr in self.TR_list:
        #     Anal()
        #     Depl()
        #     tmin += 1



    @staticmethod
    def spotX_on_RSC_loaded(x, rsc, from_end=False):
        # obecnie trzeba zapodać na selfie LTS.Manage
        # Nie trzeba dawać 10. Można dać 2. Lub 3. Lub 7. Cokolwiek
        if len(rsc.loaded) == 0: print('Brak modułów w podanym zasobie')
        if from_end == False:
            if len(rsc.loaded) > x:
                for i in range(x):
                    print(rsc.loaded[i].name, rsc.loaded[i].kind,
                          rsc.loaded[i].project, rsc.loaded[i].time,
                          rsc.loaded[i].status, rsc.loaded[i].temp)
            elif len(rsc.loaded) > 0:
                for i in range(len(rsc.loaded)):
                    print(rsc.loaded[i].name, rsc.loaded[i].kind,
                          rsc.loaded[i].project, rsc.loaded[i].time,
                          rsc.loaded[i].status, rsc.loaded[i].temp)
        else:
            if len(rsc.loaded) > x:
                for i in range(x):
                    print(rsc.loaded[-i].name, rsc.loaded[-i].kind,
                          rsc.loaded[-i].project, rsc.loaded[-i].time,
                          rsc.loaded[-i].status, rsc.loaded[-i].temp)
            elif len(rsc.loaded) > 0:
                for i in range(len(rsc.loaded)):
                    print(rsc.loaded[-i].name, rsc.loaded[-i].kind,
                          rsc.loaded[-i].project, rsc.loaded[-i].time,
                          rsc.loaded[-i].status, rsc.loaded[-i].temp)
        return None
        # ahh, jakaż okazja by to przerobić na generatorek


    # generatorki do obrobienia jeszcze - moze sie przyda:
    def gen_ALL_RSCs(self, t_qty, tc_qty, tc_cap, tr_qty, at_qty):
        self.gen_Trunk()
        self.gen_Tests(t_qty)
        self.gen_Storage()
        self.gen_TCs(tc_qty, tc_cap)
        self.gen_TRs(tr_qty)
        self.gen_ATs(at_qty)
        #cdn

    def gen_Trunk(self):
        trumna = RSC_trunk('TrumnaAPA')
        self.other_RSC.append(trumna)
        print('Utworzono TrumnaAPA')
        return None

    def gen_Tests(self, qty):
        for i in range(qty):
            test_name = 'Test{}'.format(i + 1)
            self.test_list.append(Modulet(test_name))
        print('Dodano(utworzono)', qty, 'testów do \'test_list\'y')
        return None

    def gen_Storage(self):
        storage = RSC_Store('StorageLAB')
        self.other_RSC.append(storage)
        print('Utworzono strefe StorageLAB')
        return None

    def gen_TCs(self, qty, cap):
        self.TC_list.append(RSC_TC('TC_RT', 23))
        for i in range(qty):  # robimy komory
            tc = 'TC_{}'.format(i+1)
            temps = [-35, 85]
            self.TC_list.append(RSC_TC(tc, temps[1 if 3 * i % 2 == 0 else 0]))
                # zwraca zawsze 0 lub 1 o ile sie nie jebnałem, bo kótka
                # lista temps i dla wiekszej iloci komor nie chciałem komplikowac
                # aż tak temp- do ustawiania wedle potrzeb razem z tempsem
            self.TC_list[-1].set_max_in(cap)
        print('Utworzono komory TC_1 do TC_%s' %(qty))

    def gen_TRs(self, tr_qty, wich_qty=0):

        for i in range(tr_qty):  # robimy TRy
            tr = 'TR_{}'.format(i+1)
            self.TR_list.append(RSC_TR(tr))
            self.TR_list[-1].set_max_in(1)
        print('Utworzono TestRoomy TR_1 do TR_%s' %(tr_qty))
        if wich_qty > 0:
            for i in range(wich_qty):  # robimy WICHy
                w = 'WICH_{}'.format(i+1)
                self.TR_list.append(RSC_TR(w, IN=True))
                self.TR_list[-1].set_max_in(1)
            print('Utworzono komory testowe WICH_1 do WICH_%s' %(tr_qty))

    def gen_ATs(self, at_qty):
        for i in range(at_qty):  # robimy komory
            at = 'AT_{}'.format(i+1)
            self.AT_list.append(RSC_Analysis(at))
            self.AT_list[-1].set_max_in(1)
        print('Utworzono Stanowiska Analizy AT_1 do AT_%s' %(at_qty))


class Time:
    time_formats = {'min': 1,
                    'hrs': 60,
                    'day': 1440,
                    'mnt': 33120,
                    'yer': 397440
                    }

    def __init__(self, test_list, time_format='min', value=None):
        self.cols = ['Delivery', 'Trumna', 'Check_in', 'Storage', 'Conditioning',
                     'TC', 'Deployment', 'TR', 'Analisys', 'AT',
                     'Final', 'Fin_queue', 'kind', 'project', 'temp', 'result']
        self.test_list = test_list
        self.time_format = time_format
        self.value = value
        self.time_init = 0
        self.real_time = 0
        self.log = pd.DataFrame(columns=self.cols, index=self.test_list)
        #self.log = pd.DataFrame(columns=self.cols, index=[test.name for test in self.test_list)

    def add_event_time_log(self, modulet, event, time, rsc, paramy=None, result=None):
        """
        Dodawanie informacji do logu przy zmianie statusu
        :param modulet: test do zaktualizowania, chyba test jako object a nie test.name tylko nie wiem jak to się zachowa
        :param event: nazwa eventu, najlepiej chyba nazwa statusu bo bedzie pod ręką
        :param time: czas zmiany statusu, real_time
        :param rsc: lista z dwiema pozycjami, [nazwa rsc w której nastąpiła zmiana statusu, rsc do którego moduł jest wrzucany(np. komora TC2)]
        :param paramy: lista z parametrami do wpisania, defaultowo None, dokładniej chodzi o [kind, projekt, temp], chyba dodawane przy check_in
        :param result: ocena, dodawana przy evencie analisys
        :return: nic
        """
        self.log.loc[modulet][event] = time
        self.log.loc[modulet][rsc[0]] = rsc[1]
        if paramy:
            self.log.loc[modulet][12:15] = paramy

    def add_time_module(self, modulet):
        self.modulet = modulet

    def add_real_time(self, counter):
        self.real_time += counter

    def check_time(self):
        return self.real_time

    def time_converter(self, time):
        t = time * self.time_formats[self.time_format]
        return t




class Event:
    def __init__(self, pull_from, push_to, event_time):

        self.pull_from = pull_from
        self.push_to = push_to
        self.event_time = event_time
        self.log = None

    def add_time(self, module):
        # uzywana w run_event do zmiany czasu odwoluje sie do
        # funkcji o tej samej nazwie w Modulet
        module.add_time(self.event_time)

    def add_to_log(self, module):
        log = {module.time: ['Event', module]}
        module.add_to_log(log)


    def run_event(self):
        # dodaje do kontenera klasy RSC elementy z listy zrodlowej
        # zaczynając od poczatku listy
        # predefiniowanych(rodzaj RSC, lista zrodlowa) osobno
        # dla poszczegolnych eventów. W przypadku uzycia argumentu
        # module_qty narzucony jest limit przenoszonych testów

        def run_update_tparams():
            t = self.pull_from.loaded.pop(0)



            self.add_to_log(t)
            self.push_to.load(t)
            self.add_time(t)

        if self.push_to.max_in == False:
            while len(self.pull_from.loaded) > 0:
                run_update_tparams()
        else:
            while len(self.pull_from.loaded) > 0 and \
                    self.push_to.max_in - len(self.push_to.loaded) > 0:
                run_update_tparams()


class RSC:

    '''klasa bazowa dla obiektow z grupy ReSourCes'''
    def __init__(self, max_in=False):
        self.max_in = max_in
        self.loaded = []
        self.time = 0

    def set_max_in(self, new_val):
        # Funkcja przyjmuje jedynie jeden lub dwa argumenty liczbowe
        # self.max_in = new_val
        if new_val > len(self.loaded):
            self.max_in = new_val
        else:
           self.in_queue = self.loaded[new_val:] + self.in_queue
           self.loaded =  self.loaded[:new_val]
           self.max_in = new_val

    def load(self, test):
        #zaladuj jesli jest miejsce, jak nie to zaladuj do kolejki
        if self.max_in == False:
            self.loaded.append(test)
        elif len(self.loaded) < self.max_in:
            self.loaded.append(test)


class Transport(Event):
    '''
    Klasa symulująca transport:
    ilosć wysztskich modułów przewidzianych na testy
    podzielona na trumny o losowej pojemnosci z określonego zakresu (symulacja produkcji)
    wysyłanych ustaloną ilość razy na dobę
    '''
    def __init__(self, *args):
        super(Transport, self).__init__(*args)

    def run_event(self):
        # dodaje do kontenera klasy RSC elementy z listy zrodlowej
        # zaczynając od poczatku listy
        # predefiniowanych(rodzaj RSC, lista zrodlowa) osobno
        # dla poszczegolnych eventów. W przypadku uzycia argumentu
        # module_qty narzucony jest limit przenoszonych testów

        def run_update_tparams():
            t = self.pull_from.pop(0)
            t.status = 'Delivery'
            self.add_to_log(t, )
            self.push_to.load(t)
            self.add_time(t)

        if self.push_to.max_in == False:
            while len(self.pull_from) > 0:
                run_update_tparams()
        else:
            while len(self.pull_from) > 0 and self.push_to.max_in - len(self.push_to.loaded) > 0:
                run_update_tparams()


class RSC_trunk(RSC):
    '''klasa definiujaca trumne'''

    def __init__(self, name, *args, **kws):
        super(RSC_trunk, self).__init__(**kws)
        # Klasa przyjmuje jedynie jeden lub dwa argumenty liczbowe
        self.name = name
        if len(args) > 2:
            args = args[:2]
        if args:
            if len(args) == 1:
                super(RSC_trunk, self).set_max_in(args[0])
            elif len(args) == 2:
                rand_val = np.random.randint(args[0], args[1])
                super(RSC_trunk, self).set_max_in(rand_val)


class Check_in(Event):
    '''
    klasa symulująca przyjęcie modułów,
    w obrębie której nastepuje losowanie ratingów, in/out, , temperatur, cond_time i innych atrybutów skojarzonych z modułem
    zmiana statusu na 'x'
    '''
    project_qty = 3
    def __init__(self, *args):
        super(Check_in, self).__init__(*args)

    def set_project_qty(self, qty):
        self.project_qty = qty

    def gen_rand_testparam(self, test):
        # funkcja losujaca parametry testów
        test.project = random.randint(1, self.project_qty)

        # losowanie in/out -> modulet
        test.kind = random.choice(Modulet.ab_kind)
        test.temp = np.random.choice([-35, -30, 23, 60, 85, 90], 1, p=[0.25, 0.15, 0.25, 0.03, 0.25, 0.07])
        #tu ewentualnie obsługa ratingów, tylko gdzie je zapisywać?
        # if str(test.project) in Manage.ratings.keys():
        #     print('kupa')
        #     # TODO: OBSŁUŻYĆ KUPSZTALA
        # else: test.temp = random.choice([-35, 23, 85])

    def run_event(self, module_qty=False):
        # dodaje do kontenera klasy RSC elementy z listy zrodlowej
        # zaczynając od poczatku listy
        # predefiniowanych(rodzaj RSC, lista zrodlowa) osobno
        # dla poszczegolnych eventów. W przypadku uzycia argumentu
        # module_qty narzucony jest limit przenoszonych testów

        def run_update_tparams():
            t = self.pull_from.loaded.pop(0)
            self.gen_rand_testparam(t) # nadajemy losowe parametry
            t.status = 'Checked in' # updateujemy status
            self.add_to_log(t)    # updatujemy logi
            self.push_to.load(t)  # przenosimy miedzy zasobami
            self.add_time(t)      # updateujemy self.time modulu

        if self.push_to.max_in == False:
            while len(self.pull_from.loaded) > 0:
                # print('max in = False & mod_qty = False')
                run_update_tparams()
        else:
            while len(self.pull_from.loaded) > 0 and \
                self.push_to.max_in - len(self.push_to.loaded) > 0:
                    # print('max in = True & mod_qty = False')
                run_update_tparams()


class RSC_Store(RSC):
    '''Tam gdzie skladowane sa testy a w oddali majacza swiatła mordoru'''
    def __init__(self, name):
        super(RSC_Store, self).__init__()
        self.name = name

    def temp_count(self, limit=0):
        te_lst = []
        tl = []
        tc = {}

        for test in self.loaded:
            te_lst.append(test.temp)
            if  not test.temp in tl:
                tl.append(test.temp)
        for temp in tl:
            tc.update({temp : te_lst.count(temp)})


        print(tc, sum(tc.values()))



class Conditioning(Event):
    '''
    klasa symulująca kondycjonownie modułu w okreslonyh z góry częstościach uzupełniania komór,
    ich pojemnościach i temperaturach.
    '''
    rdylst = []


    def run_event(self):

        # TODO: czy sprawdzenie 'len(chamber.loaded) < chamber.max_in' jest poprawne??
        # TODO: w tym momencie sprawdzamy załadowanie konkretnej komory (komora ma większe cap niż np. te 8) i może się zdażyć że w jednej będzie 14 modułów a w drugiej 2 moduły (suma 16 czyli ok na dwa TR), a na ten moment mamy że musi być 8 + 8.
        # TODO: może zamiast tego, sprawdzać czy suma wrzuconych modułów jest mniejsza niż maks na TRy i potem czy maks cap (Ale to realne cap TC) TC jest większe od loaded
        l = []
        if len(self.pull_from.loaded) > 0: # spr czy jest co brac
            # oraz spr czy jest po co wrzucac
            # (suma po tc.loaded vs len trlist
            for test in self.pull_from.loaded:
                for chamber in self.push_to:
                    if test.temp == chamber.temp:
                        #może coś takiego??
                        # TODO: if len(self.puch_to) < len(tr_list)*(frq_check_in/deploy_time)
                        if len(chamber.loaded) < chamber.max_in or chamber.max_in == False:
                            if test not in l:
                                chamber.load(test)
                                self.add_to_rdylst(test)
                                l.append(test)
                                test.status = 'Conditioning'
                                self.add_to_log(test)
                                if test.temp != 23:
                                    self.add_time(test)



        for item in l:
            if item in self.pull_from.loaded:
                self.pull_from.loaded.remove(item)

        for TC in self.push_to:
            print(TC.loaded)

    def add_to_rdylst(self, test):
        self.rdylst.append(test)


class RSC_TC(RSC):
    '''klasa definiujaca obiekty TemperatureChambers'''
    def __init__(self, name=None, temp=None):
        self.name = name
        self.temp = temp
        super(RSC_TC, self).__init__()

    def set_temp(self, temp):
        self.temp = temp

    def set_name(self, name):
        self.name = name


class Deployment(Event):
    '''
    Klasa symulująca przeprowandzenia testu. Zmiana statusu
    W jej obebie mają znajdować sie TR oraz WICH (dodatkowy czas 30 minut dokondycjonowania doliczany w tym typie)
    '''
    # def __init__(self, *args, **kws):
    #     super(Deployment, self).__init__(*args, **kws)

    def run_event(self):

        l = []
        for test in Conditioning.rdylst:
            for tr in self.push_to:
                if len(tr.loaded) < tr.max_in:
                    tr.load(test)
                    l.append(test)
                    test.status = 'DEPLOYMENT'
                    self.add_time(test)
                    self.add_to_log(test)

        for item in l:
            for j in range(len(self.pull_from)):
                    chamber = self.pull_from[j]
                    if item in chamber.loaded:
                        chamber.loaded.remove(item)
            for k in range(len(Conditioning.rdylst)):
                if item in Conditioning.rdylst:
                    Conditioning.rdylst.remove(item)


class RSC_TR(RSC):
    '''Pomieszczenia testowe'''
    def __init__(self, name, IN=False, *args, **kws):
        self.name = name
        self.IN = IN
        super(RSC_TR, self).__init__()

    def load(self, test):
        #zaladuj jesli jest miejsce, jak nie to zaladuj do kolejki
        if self.max_in == False:
            self.loaded.append(test)
        elif len(self.loaded) < self.max_in:
            self.loaded.append(test)
        elif len(self.loaded) >= self.max_in:
            self.in_queue.append(test)

class Analysis(Event):
    '''
    zmiana statusu na finalny, dodanie oceny testu.
    '''

    def run_event(self, check_time): # jak pobrać czas? to działa ale pycharm podkreśla
        check_time
        # do przeróbyyyyyy
        l, k = [], []
        print(check_time)
        if check_time > 0:
            for tr in self.pull_from:  # z listy test roomow
                for test in tr.loaded:  # z kazdego tr pobierz test
                    self.push_to[0].in_queue.append(test)
                    k.append(test)  # i wrzuc do koljki
                for item in k:
                    for i in range(len(tr.loaded)):
                        if item in tr.loaded:
                            tr.loaded.remove(item)

        for at in self.push_to:
            for test in at.in_queue:
                if len(at.loaded) < at.max_in:
                    at.load(test)
                    l.append(test)
                    test.status = 'ANALYSIS'
                    test.result_eval = np.random.choice(['OK', 'COK', 'NOK'], 1, p=[0.7, 0.2, 0.1])
                    self.add_time(test)
                    self.add_to_log(test)
            for item in l:
                for j in range(len(at.in_queue)):
                    if item in at.in_queue:
                        at.in_queue.remove(item)
                        at.finit.append(item)


class RSC_Analysis(RSC):
    '''Analysis Tables'''
    in_queue = [] #bo kolejka do stołów jest jedna
    finit = []
    def __init__(self, *args, **kwargs):
        super(RSC_Analysis, self).__init__(*args, **kwargs)


    def add_queue(self, testobj):
        self.in_queue.append(testobj)

    def del_queue(self, testobj):
        self.in_queue.remove(testobj)


class Modulet:
    '''
    klasa w obrębie której będą bedą gromadzić się parametry uzyskiwane w poszczególnych etapach procesu.
    '''

    project_rat = {} # zbiera projekty
    rating_list = {} # zbiera na piwo
    project_rcount = {}


    ab_kind = 'dab pab sab kab ic'.upper().split()

    def __init__(self, name):
        """
        :param times: czas życia modułu, zwiększany przy zmianie statusu
        :param status: status modułu, zmieniany z każdym etapem
        :param kind: randomowy numer, który będzie definiował rodzaj poduszki.[ random.randint(0, len(ab_king)) ]
        :param eval: ocena testu ['OK', 'NOK', 'INVALID']
        :param project: liczba określająca projekt (jedna liczba == jeden projekt) generowana z podanego zakresu
        :param args: dodatkowe argumenty których zapomniałem zamieścić
        :param IO: parametr IN == True lub OUT == False (domyślnie False)
        """
        self.name = name
        self.time = 0
        self.status = None
        self.kind = None
        self.project = None
        self.temp = None
        self.result_eval = False
        self.log = {}
        #rsc redy robi sie w conditioning

    def gen_proj_rat(self):
        pass

    def gen_rand_rat(self, temps=False, spread=2):
        # SPR CZY JEST RATING DLA PROJ I DODANIE JESLI NEI MA

        if not self.project in self.project_rat.keys():
            if temps == False:
                temps = [-35, 23, 85]
            rv = []
            for i in range(len(temps)):
                rv.append(np.random.randint(1, spread+1))
            if rv.count(rv[0]) == len(rv):
                rv = [1 for x in range(len(rv))]

            self.project_rat[self.project] = rv

    def r_scn(self):
        for t, q in zip(self.project_rat[self.project],
                 self.project_rcount[self.project]):
            for tx, qx in zip(t, q):
                if self.time == tx:
                    print(qx)

    def get_temp_from_rat(self):
        # nadaje temp na podst ratingu

        tqxcount = ((t.count(tx)/len(t))/(qx/sum(q))
                    for t, q in zip(self.project_rat[self.project],
                                    self.project_rcount[self.project])
                    for tx, qx in zip(t, q))

        print(filter(min, tqxcount))


    def my_time(self):
        #pokaz swoj czas
        return self.time

    def add_time(self, event_time):
        self.time += event_time

    def add_to_log(self, test_ev):
        self.log.update(test_ev)


def randoms_from_sum(number, *args):

    '''
    Funkcja zwracająca losowe wartości których suma wynosi 'number'
    :param number: Suma wygenerowanych losowo wartości
    :param args_max: określa zakres maxymalny z którego wartości są dobierane
    :return: 
    '''
    rand_list = []

    while sum(rand_list) < number - 1:
        total = number - sum(rand_list)
        rand_num = (np.random.randint(*args) if args else np.random.randint(total))

        if rand_num is not 0:
            if rand_num >= total:
                rand_num = total
            rand_list.append(rand_num)

    if sum(rand_list) + 1 == number: rand_list[-1] += 1

    return rand_list


def spread_from_sum(number, spread, *args):
    '''
    Funkcja generuje wartości których suma wynosi number a ilość wynosi spread
    :param number: 
    :param spreads: 
    :return: 
    '''

    rand_list = []
    x = int(number / spread)
    i = 1

    while sum(rand_list) < number:
        while i < spread:
            y = np.random.choice([-1, 1]) * (np.random.randint(*args) if args else np.random.randint(x))
            z = x + y
            if z + sum(rand_list) > number or z <= 0:
                break
            rand_list.append(z)
            i += 1
        if i == spread:
            z = number - sum(rand_list)
            rand_list.append(z)

    return rand_list

#######################################
    # import LTS
    # mng = LTS.Manage(100, 3, 8, 4, 4)
    #
    # Trumna = mng.other_RSC[0]
    # Storage = mng.other_RSC[1]
    #
    # # print(mng.test_list, '\n\n',
    # #       mng.other_RSC, '\n\n',
    # #       mng.TC_list, '\n\n',
    # #       mng.TR_list)
    #
    # LTS.Transport(mng.test_list, Trumna, 60).run_event()
    # LTS.Manage.spotX_on_RSC_loaded(1, Trumna, True)
    # LTS.Check_in(Trumna, Storage, 20).run_event()
    # Storage.temp_count()
    # LTS.Conditioning(Storage, mng.TC_list, 240).run_event()
    # Storage.temp_count()
    # for tc in mng.TC_list:
    #     print('%s : %s : %s : %s' % (tc.name, tc.temp, len(tc.loaded), tc.max_in))
    # LTS.Deployment(mng.TC_list, mng.TR_list, 15).run_event()
    # print('Aktualnie testowane w ', mng.TR_list[0].name)
    # LTS.Manage.spotX_on_RSC_loaded(1, mng.TR_list[0])
    # LTS.Analysis(mng.TR_list, mng.AT_list, 15).run_event()
    # LTS.Manage.spotX_on_RSC_loaded(1, mng.AT_list[0])

    # #####################