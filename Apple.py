import pygame
import random

class Apple():
    def __init__(self,rozmiar_Kratki,szerokosc_Kratki,wysokosc_Kratki):
        self.pozycja = (0, 0)
        self.kolor = (255, 0, 0)
        self.rozmiar_Kratki = rozmiar_Kratki
        self.szerokosc_Kratki = szerokosc_Kratki
        self.wysokosc_Kratki = wysokosc_Kratki
        self.pozycja_Losowa()


    def pozycja_Losowa(self):
        self.pozycja = (random.randint(0, self.szerokosc_Kratki - 1) * self.rozmiar_Kratki, random.randint(0, self.wysokosc_Kratki - 1) * self.rozmiar_Kratki)

    def rysuj(self, okno_Gry):
        r = pygame.Rect((self.pozycja[0], self.pozycja[1]), (self.rozmiar_Kratki, self.rozmiar_Kratki))
        pygame.draw.rect(okno_Gry, self.kolor, r)