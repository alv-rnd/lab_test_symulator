import pandas as pd
import numpy as np

class Manage:
    '''
    Klasa zarządzająca wszytkim
    '''

class Transport:
    '''
    Klasa symulująca transport:
    ilosć wysztskich modułów przewidzianych na testy
    podzielona na trumny o losowej pojemnosci z określonego zakresu (symulacja produkcji)
    wysyłanych ustaloną ilość razy na dobę
    '''
class Check_in:
    '''
    klasa symulująca przyjęcie modułów,
    w obrębie której nastepuje losowanie ratingów, in/out, , temperatur, cond_time i innych atrybutów skojarzonych z modułem
    zmiana statusu na 'x'
    '''
class Conditioning:
    '''
    klasa symulująca kondycjonownie modułu w okreslonyh z góry częstościach uzupełniania komór,
    ich pojemnościach i temperaturach.
    '''
class Deployment:
    '''
    Klasa symulująca przeprowandzenia testu. Zmiana statusu
    W jej obebie mają znajdować sie TR oraz WICH (dodatkowy czas 30 minut dokondycjonowania doliczany w tym typie)
    '''
class Analysis:
    '''
    zmiana statusu na finalny, dodanie oceny testu.
    '''
class Modulet:
    '''
    klasa w obrębie której będą bedą romadzić się parametry uzyskiwanie w poszczególnych etapach procesu.
    
    '''