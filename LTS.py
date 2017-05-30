# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import random
import os


class Manage:
    init = False
    '''
    Klasa zarządzająca wszytkim
    '''
    # ratings = {'1': [[1, 2, 1], [0, 0, 0]],
    #            '2': [[1, 1, 1], [0, 0, 0]],
    #            '3': [[2, 1, 1], [0, 0, 0]]}
    # Lista zdarzeń do sprawdzenia kolejnego zdarzenia ktore
    # mozna wykonac: petla while (np) leci po kazdym dodanym resourcie
    # i spr rsc.in_queue lub .loaded (jedno z dwojga zaleznie od podejsia)
    # i jezeli taka lista jest nie pusta odnajduje zaciagajacy lub wypychajacy
    # event - albo zupełnie inaczej - np. eventy wyzwalaja
    # sasiadujce eventy miedzy soba z automatu, albo
    # roznie w zależności od rodzju procesu
    def __init__(self, t_qty, tc_qty, tc_cap):
        self.t_qty = t_qty
        self.tc_qty = tc_qty
        self.tc_cap = tc_cap
        self.test_list = []
        self.other_RSC =[]
        self.TC_list = []
        self.TR_list = []
        self.gen_ALL_RSCs(self.t_qty, self.tc_qty, self.tc_cap)
        self.real_time = Time()

    def sim_run(self):
        check = self.real_time.check_time()
        self.init = True
        while self.init:
            if check == 0 or check %


    def set_max_in(self, rsc_name, new_val):
        # Funkcja - RSC - do zmian argumentu max_in(new_val)
        pass
        # RSC_trunk(rsc_name).set_max_in

    # podglad modułów w danym zasobie RSC
    def spotX_on_RSC_loaded(self, x, rsc, from_end=False):
        # obecnie trzeba zapodać na selfie LTS.Manage(10)
        # Nie trzeba dawać 10. Można dać 2. Lub 3. Lub 7. Cokolwiek
        if len(rsc.loaded) == 0: print('Brak modułów w podanym zasobie')
        if from_end:
            if len(rsc.loaded) > x:
                for i in range(x):
                    print(rsc.loaded[i].name, rsc.loaded[i].type,
                          rsc.loaded[i].project, rsc.loaded[i].temp)
            elif len(rsc.loaded) > 0:
                for i in range(len(rsc.loaded)):
                    print(rsc.loaded[i].name, rsc.loaded[i].type,
                          rsc.loaded[i].project, rsc.loaded[i].temp)
        else:
            if len(rsc.loaded) > x:
                for i in range(x):
                    print(rsc.loaded[-i].name, rsc.loaded[-i].type,
                          rsc.loaded[-i].project, rsc.loaded[-i].temp)
            elif len(rsc.loaded) > 0:
                for i in range(len(rsc.loaded)):
                    print(rsc.loaded[-i].name, rsc.loaded[-i].type,
                          rsc.loaded[-i].project, rsc.loaded[-i].temp)
        # ahh, jakaż okazja by to przerobić na generatorek


    # generatorki do obrobienia jeszcze - moze sie przyda:
    def gen_ALL_RSCs(self, t_qty, tc_qty, tc_cap):
        self.gen_Trunk()
        self.gen_Tests(t_qty)
        self.gen_Storage()
        self.gen_TCs(tc_qty, tc_cap)
        #cdn

    def gen_Trunk(self):
        trumna = RSC_trunk()
        self.other_RSC.append(trumna)
        return None

    def gen_Tests(self, qty):
        for i in range(qty):
            test_name = 'Test{}'.format(i + 1)
            self.test_list.append(Modulet(test_name))
        print('Dodano(utworzono)', qty, 'testów do \'test_list\'y')
        return self.test_list

    def gen_Storage(self):
        Storage = RSC_Store()
        self.other_RSC.append(Storage)
        print('Utworzono strefe ', Storage, 'wielką i nieskończoną. Na horyzoncie widać Mordor')
        return None

    def gen_TCs(self, qty, cap):
        for i in range(qty):  # robimy komory
            tc = 'TC_{}'.format(i)
            temps = [-35, 85]
            self.TC_list.append(RSC_TC(tc, temps[1 if 3 * i % 2 == 0 else 0]))
                # zwraca zawsze 0 lub 1 o ile sie nie jebnałem, bo kótka
                # lista temps i dla wiekszej iloci komor nie chciałem komplikowac
                # aż tak temp- do ustawiania wedle potrzeb razem z tempsem
            self.TC_list[-1].set_max_in(cap)
        print('Utworzono komory TC_1 do TC_%s' %(qty))


class Time:
    time_formats = ['sek', 'min', 'hrs', 'day', 'mnt', 'yer']
    def __init__(self, time_format='min', value=None):
        self.time_format = time_format
        self.value = value
        self.time_init = 0
        self.real_time = 0

    def add_time_module(self, modulet):
        self.modulet = modulet

    def check_time(self):
        return self.real_time
        # current_general_time = self.time_init +

    def make_log(self):
        pass
        #log = pd


class Event:
    def __init__(self, pull_from, push_to, event_time):

        self.pull_from = pull_from
        self.push_to = push_to
        self.event_time = event_time

    def add_time(self, module):
        # uzywana w run_event do zmiany czasu odwoluje sie do
        # funkcji o tej samej nazwie w Modulet
        module.add_time(self.event_time)

    def add_to_log(self, module):
        log = {module.time: ['Event', module]}
        module.add_to_log(log)

    def run_event(self, module_qty=False):
        # dodaje do kontenera klasy RSC elementy z listy zrodlowej
        # zaczynając od poczatku listy
        # predefiniowanych(rodzaj RSC, lista zrodlowa) osobno
        # dla poszczegolnych eventów. W przypadku uzycia argumentu
        # module_qty narzucony jest limit przenoszonych testów

        def run_Forest():
            t = self.pull_from.loaded.pop(0)

            self.add_to_log(t)
            self.push_to.load(t)
            self.add_time(t)

        if self.push_to.max_in == False:
            if module_qty == False:
                while len(self.pull_from.loaded) > 0:
                    #print('max in = False & mod_qty = False')
                    run_Forest()
            else:
                while len(self.pull_from.loaded) > 0 and module_qty > 0:
                    #print('max in = False & mod_qty = True')
                    run_Forest()
                    module_qty -= 1
        else:
            if module_qty == False:
                while len(self.pull_from.loaded) > 0 and \
                                        self.push_to.max_in - len(self.push_to.loaded) > 0:
                    #print('max in = True & mod_qty = False')
                    run_Forest()
            else:
                while len(self.pull_from.loaded) > 0 and module_qty > 0 and \
                                        self.push_to.max_in - len(self.push_to.loaded) > 0:
                    #print('max in = True & mod_qty = True')
                    run_Forest()


class RSC:

    '''klasa bazowa dla obiektow z grupy ReSourCes'''
    def __init__(self, max_in=False):
        self.max_in = max_in
        self.in_queue = []
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

    def add_queue(self, testobj):
        self.in_queue.append(testobj)

    def del_queue(self, testobj):
        self.in_queue.remove(testobj)

    def load(self, test):
        #zaladuj jesli jest miejsce, jak nie to zaladuj do kolejki
        if self.max_in == False:
            self.loaded.append(test)
        elif len(self.loaded) < self.max_in:
            self.loaded.append(test)
        else:
            self.in_queue.append(test)
        # TODO: przekazywanie informacji do logów
        # TODO: obsluga czasow


class Transport(Event):
    '''
    Klasa symulująca transport:
    ilosć wysztskich modułów przewidzianych na testy
    podzielona na trumny o losowej pojemnosci z określonego zakresu (symulacja produkcji)
    wysyłanych ustaloną ilość razy na dobę
    '''
    def __init__(self, *args):
        super(Transport, self).__init__(*args)

    def run_event(self, module_qty=False):
        # dodaje do kontenera klasy RSC elementy z listy zrodlowej
        # zaczynając od poczatku listy
        # predefiniowanych(rodzaj RSC, lista zrodlowa) osobno
        # dla poszczegolnych eventów. W przypadku uzycia argumentu
        # module_qty narzucony jest limit przenoszonych testów

        def run_Forest():
            t = self.pull_from.pop(0)

            self.add_to_log(t)
            self.push_to.load(t)
            self.add_time(t)

        if self.push_to.max_in == False:
            if module_qty == False:
                while len(self.pull_from) > 0:
                    run_Forest()
            else:
                while len(self.pull_from) > 0 and module_qty > 0:
                    run_Forest()
                    module_qty -= 1
        else:
            if module_qty == False:
                while len(self.pull_from) > 0 and \
                    self.push_to.max_in - len(self.push_to.loaded) > 0:
                    run_Forest()
            else:
                while len(self.pull_from) > 0 and module_qty > 0 and \
                    self.push_to.max_in - len(self.push_to.loaded) > 0:
                    run_Forest()

class RSC_trunk(RSC):
    '''klasa definiujaca trumne'''

    def __init__(self, *args, **kws):
        super(RSC_trunk, self).__init__(**kws)
        # Klasa przyjmuje jedynie jeden lub dwa argumenty liczbowe

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
        test.project = random.randint(1, self.project_qty + 1)
        test.type = random.choice(Modulet.ab_kind)
        test.temp = random.choice([-35, 23, 85])
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

        def run_Forest():
            t = self.pull_from.loaded.pop(0)
            self.gen_rand_testparam(t) # nadajemy losowe parametry
            t.status = 'Checked in' # updateujemy status
            self.add_to_log(t)    # updatujemy logi
            self.push_to.load(t)  # przenosimy miedzy zasobami
            self.add_time(t)      # updateujemy self.time modulu

        if self.push_to.max_in == False:
            if module_qty == False:
                while len(self.pull_from.loaded) > 0:
                    # print('max in = False & mod_qty = False')
                    run_Forest()
            else:
                while len(self.pull_from.loaded) > 0 and module_qty > 0:
                    # print('max in = False & mod_qty = True')
                    run_Forest()
                    module_qty -= 1
        else:
            if module_qty == False:
                while len(self.pull_from.loaded) > 0 and \
                                        self.push_to.max_in - len(self.push_to.loaded) > 0:
                    # print('max in = True & mod_qty = False')
                    run_Forest()
            else:
                while len(self.pull_from.loaded) > 0 and module_qty > 0 and \
                                        self.push_to.max_in - len(self.push_to.loaded) > 0:
                    # print('max in = True & mod_qty = True')
                    run_Forest()

    # zwiekszenie czasu w modulet
    # zmiana statusu
    # losowanie ratingów -> modulet
    # losowanie temp -> modulet
    # losowanie cond_time -> modulet
    # losowanie in/out -> modulet
    # dodanie w logu modulet (słownik?) par czas/godzina : lista statusu, oceny, czasu trwania etapu itp
    # capacity/zdolność/wydolność danego obszaru/etapu/kroku oraz kolejki???


class RSC_Store(RSC):
    '''Tam gdzie skladowane sa testy a w oddali majacza swiatła mordoru'''
    def __init__(self):
        super(RSC_Store, self).__init__()


class Conditioning(Event):
    '''
    klasa symulująca kondycjonownie modułu w okreslonyh z góry częstościach uzupełniania komór,
    ich pojemnościach i temperaturach.
    '''
    pass
    # zwiekszenie czasu w modulet
    # zmiana statusu

    # dodanie w logu modulet (słownik?) par czas/godzina : lista statusu, czasu trwania etapu itp
    # capacity/zdolność/wydolność danego obszaru/etapu/kroku oraz kolejki???


class RSC_TC(RSC):
    '''klasa definiujaca obiekty TemperatureChambers'''
    temp_range = [-40, -35, -30, -25, 23, 80, 85, 90]
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
    pass
    # zwiekszenie czasu w modulet
    # zmiana statusu

    # dodanie w logu modulet (słownik?) par czas/godzina : lista statusu, oceny, czasu trwania etapu itp
    # capacity/zdolność/wydolność danego obszaru/etapu/kroku oraz kolejki???


class RSC_TR(RSC):
    pass


class Analysis(Event):
    '''
    zmiana statusu na finalny, dodanie oceny testu.
    '''
    pass
    # zwiekszenie czasu w modulet
    # zmiana statusu
    # dodanie oceny
    # dodanie w logu modulet (słownik?) par czas/godzina : lista statusu, oceny, czasu trwania etapu itp
    # capacity/zdolność/wydolność danego obszaru/etapu/kroku oraz kolejki???


class RSC_Analysis:
    pass


class Modulet:
    '''
    klasa w obrębie której będą bedą gromadzić się parametry uzyskiwane w poszczególnych etapach procesu.
    '''
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

    def my_time(self):
        #pokaz swoj czas
        return self.time

    def add_time(self, event_time):
        self.time += event_time

    def add_to_log(self, test_ev):
        self.log.update(test_ev)



        # dodać w inicie param log - pusty słownik
        # gromadzenie logu czas: ilość moduletów w danym statusie - \
        # - ekspozycja wąskiego gardła - ewentualnie można sie bawić z df i podstawowym logiem

    # ### Funkcje: ###

        # dodać w inicie param log - pusty słownik
        # gromadzenie logu czas: ilość moduletów w danym statusie - \
        # - ekspozycja wąskiego gardła - ewentualnie można sie bawić z df i podstawowym logiem


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


# #print(spread_from_sum(100, 20))
# #print(randoms_from_sum(100, 20))
#
# import LTS
#
# def generate_test(qty, lst):
#     # na potrzeby budowy programu
#
#     for i in range(qty):
#         test_name = 'Test{}'.format(i+1)
#
#         lst.append(LTS.Modulet(test_name))
#     else:
#         test_name = None
#
# trumna = LTS.RSC_trunk()
# print('Utworzono trumne o pojemnosci: ', trumna.max_in)
#
# prod = []
# generate_test(10, prod)
# print('wygenerowano 10 testów i dodano je do listy prod')
# for test in prod:
#     print(test.project)
#
# print('Utworzono obszar Storage')
# Storage = LTS.RSC_Store()
#
# TransportAPA = LTS.Transport(prod, trumna, 60)
# print('zdefiniowano Transport o czasie ', TransportAPA.event_time, 'minut\n',\
#       'ktory obsluzy transport modulow z listy prod w kontenerze trumna')
#
# TransportAPA.run_event(10)
# print('wywolanie transportuAPA')
#
# print('Check_in przed:')
# print(trumna.loaded)
# print(Storage.loaded)
# Check_in_LAB = LTS.Check_in(trumna, Storage, 20)
# # Check_in_LAB.run_event()
# print('Check_in po:')
# print(trumna.loaded)
# print(Storage.loaded)