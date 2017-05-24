# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np


class Manage:
    '''
    Klasa zarządzająca wszytkim
    '''
    def set_max_in(self, rsc_name, new_val):
        # Funkcja - RSC - do zmian argumentu max_in
        RSC(rsc_name).set_max_in(new_val)

class RSC:
    '''klasa bazowa dla obiektow z grupy ReSourCes'''
    def __init__(self, max_in=False, in_queue=[]):
        self.max_in = max_in
        self.in_queue = in_queue
        self.time = 0
    def set_max_in(self, new_val):
        self.max_in = new_val
    def add_queue(self, testobj):
        self.in_queue.append(testobj)
    def del_queue(self, testobj):
        self.in_queue.__delitem__(testobj)


class Transport:
    '''
    Klasa symulująca transport:
    ilosć wysztskich modułów przewidzianych na testy
    podzielona na trumny o losowej pojemnosci z określonego zakresu (symulacja produkcji)
    wysyłanych ustaloną ilość razy na dobę
    '''
    pass
    # wywoływana przez klase Menage co 24h/ilość transportów
    # zmiana statusu

    # capacity/zdolność/wydolność danego obszaru/etapu/kroku oraz kolejki???
class RSC_trunk(RSC):
    def set_max_in(self, *args):
        print('start')
        if len(*args) == 1:
            print('if 1')
            super(RSC_trunk, self).set_max_in(*args[0])
        elif len(*args) == 2:
            print('if 2')
            rand_val = np.random.randint(list(*args).sort())
            super(RSC_trunk, self).set_max_in(rand_val)
        else:
            return 'funkcja przyjmuje tylko jeden lub dwa argumenty'

class Check_in:
    '''
    klasa symulująca przyjęcie modułów,
    w obrębie której nastepuje losowanie ratingów, in/out, , temperatur, cond_time i innych atrybutów skojarzonych z modułem
    zmiana statusu na 'x'
    '''
    pass
    # zwiekszenie czasu w modulet
    # zmiana statusu
    # losowanie ratingów -> modulet
    # losowanie temp -> modulet
    # losowanie cond_time -> modulet
    # losowanie in/out -> modulet
    # dodanie w logu modulet (słownik?) par czas/godzina : lista statusu, oceny, czasu trwania etapu itp
    # capacity/zdolność/wydolność danego obszaru/etapu/kroku oraz kolejki???

class RSC_Store:
    pass

class Conditioning:
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

class Deployment:
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

class Analysis:
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

    def __init__(self, times, status, kind, eval, project, *args, IO=False):
        """
        :param times: czas życia modułu, zwiększany przy zmianie statusu
        :param status: status modułu, zmieniany z każdym etapem
        :param kind: randomowy numer, który będzie definiował rodzaj poduszki.[ random.randint(0, len(ab_king)) ]
        :param eval: ocena testu ['OK', 'NOK', 'INVALID']
        :param project: liczba określająca projekt (jedna liczba == jeden projekt) generowana z podanego zakresu
        :param args: dodatkowe argumenty których zapomniałem zamieścić
        :param IO: parametr IN == True lub OUT == False (domyślnie False)
        """
        self.times = times
        self.status = status
        self.kind = kind
        self.eval = eval
        self.project = project

        # dodać w inicie param log - pusty słownik
        # gromadzenie logu czas: ilość moduletów w danym statusie - \
        # - ekspozycja wąskiego gardła - ewentualnie można sie bawić z df i podstawowym logiem

    ### Funkcje: ###

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