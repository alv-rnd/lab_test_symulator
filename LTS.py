# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import random


class Manage:
    '''
    Klasa zarządzająca wszytkim
    '''
    event_sequence = ['Transport', 'Check_in', 'Conditioning',\
                      'Deployment', 'Analysis']
    # Lista zdarzeń do sprawdzenia kolejnego zdarzenia ktore
    # mozna wykonac: petla while (np) leci po kazdym dodanym resourcie
    # i spr rsc.in_queue lub .loaded (jedno z dwojga zaleznie od podejsia)
    # i jezeli taka lista jest nie pusta odnajduje zaciagajacy lub wypychajacy
    # event - albo zupełnie inaczej - np. eventy wyzwalaja
    # sasiadujce eventy miedzy soba z automatu, albo
    # roznie w zależności od rodzju procesu
    def __init__(self, module_qty, init=False):
        self.module_qty = module_qty
        self.init = init
        print(self.init)

    def sim_run(self):
        self.init = True
        print(self.init)
        general_time = Time()
        first_run = Transport()

    def set_max_in(self, rsc_name, new_val):
        # Funkcja - RSC - do zmian argumentu max_in
        RSC_trunk(rsc_name).set_max_in(new_val)


class Time:
    time_formats = ['sek', 'min', 'hrs', 'day', 'mnt', 'yer']
    def __init__(self, time_format='min', value=None):
        self.time_format = time_format
        self.value = value
        self.time_init = 0

    def time_add(self, event_name, event_time):
        self.event_name = event_name
        self.event_time = event_time
        current_general_time = self.time_init + event_time


class Event:
    def __init__(self, pull_from, push_to, event_time):

        self.event_time = event_time
        self.pull_from = pull_from
        self.push_to = push_to

    def run_event(self, module_qty):
        #for i in module_qty:
            # if
        pass



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
        if len(self.loaded) < self.max_in:
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

        # TODO: czy po Transport nie powinno być self?
        # TODO: sprawdziłem powinn
    def add_time(self, module):
        # uzywana w run_event do zmiany czasu odwoluje sie do funkcji o tej samej nazwie w Modulet
        module.add_time(self.event_time)

    def add_to_log(self, module):
        log = {module.time : ['transport', module]}
        module.add_to_log(log)

    def run_event(self, module_qty=0):
        # dodaje do kontenera klasy RSC elementy z listy zrodlowej
        # zaczynając od poczatku listy
        # predefiniowanych(rodzaj RSC, lista zrodlowa) osobno
        # dla poszczegolnych eventów. W przypadku uzycia argumentu
        # module_qty narzucony jest limit przenoszonych testów

        print(self.pull_from)
        while len(self.pull_from) > module_qty and\
                len(self.push_to.loaded) < self.push_to.max_in:
            t = self.pull_from.pop(0)

            self.add_to_log(t)
            self.push_to.load(t)
            self.add_time(t)

            print(t.log)
            # najpierw log, potem add tak by w logu widniał czas poczatkowy

        print(self.pull_from)
        print(self.push_to.loaded)

    # wywoływana przez klase Menage co 24h/ilość transportów
    # zmiana statusu

    # capacity/zdolność/wydolność danego obszaru/etapu/kroku oraz kolejki???

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
    def __init__(self):

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
        super(RSC, self).__init__()
        self.max_in = 1000

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


class RSC_TC:
    pass


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


class RSC_TR:
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
    ab_kind = 'dab pab sab kab ic'.split()

    def __init__(self, name, projects=4, time=0, status=0):
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
        self.time = time
        self.status = status
        self.kind = random.choice(self.ab_kind)
        self.project = str(random.randint(0, projects))
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

class GEN(type):
    '''klasa do tworzenia inastancji klasy Modulet (modul testowy'''
    def __new__(cls, name, dct={}):
        '''
        Zwraca instanje klasy Modulet na returnie
        :param name: nazwa instancji
        :param dct: argumenty jakie ma przyjac instancja - domyslnie brak
        :return: Obiekt klasy Modulet
        '''
        base = Modulet
        return type.__new__(cls, name, (base, object), dct)
    # TODO: zwracany obiekty jest klasy GEN a nie modulet
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


