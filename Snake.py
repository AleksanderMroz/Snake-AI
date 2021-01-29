

import pygame
import random
class Snake():
    def __init__(self,szerokosc_Okna_Game,wysokosc_Okna_Game,rozmiar_Kratki,szerokosc_Kratki,wysokosc_Kratki):
        self.rozmiar_Kratki = rozmiar_Kratki
        self.szerokosc_Kratki = szerokosc_Kratki
        self.wysokosc_Kratki = wysokosc_Kratki
        self.szerokosc_Okna_Game = szerokosc_Okna_Game
        self.wysokosc_Okna_Game = wysokosc_Okna_Game

        self.gora = (0, -1)
        self.dol = (0, 1)
        self.lewo = (-1, 0)
        self.prawo = (1, 0)
        self.__dlugosc = 1
        self.__pozycja = [((szerokosc_Okna_Game / 2), (wysokosc_Okna_Game / 2))]
        self.__kierunek_ruchu = self.gora
        self.punkty = 0
        self.kolor = (0, 255, 0)
        self.kolor_yellow = (255, 255, 0)
        self.kolor_1 = (0, 100, 255)
        self.kolor_2 = (0, 200, 255)
        self.kolor_3=  (124, 0, 255)



    def pozycja_Glowy(self):
        return self.__pozycja[-1]
    def get_kierunek(self):
        if self.__kierunek_ruchu==self.gora:
            return 0
        elif self.__kierunek_ruchu==self.prawo:
            return 1
        elif self.__kierunek_ruchu==self.dol:
            return 2
        elif self.__kierunek_ruchu==self.lewo:
            return 3


    def kierunek(self, kierunek_ruchu):
        # Jeśli wąż ma ogon nie może się cofnąć
        if self.__dlugosc > 1 and (kierunek_ruchu[0] * -1, kierunek_ruchu[1] * -1) == self.__kierunek_ruchu:
            return
        else:
            self.__kierunek_ruchu = kierunek_ruchu

    def ruch(self):
        glowa = self.pozycja_Glowy()
        x,y = self.__kierunek_ruchu
        # Nowa pozycja Snake na bazie pozycji jego głowy
        nowa_Pozycja = (((glowa[0] + (x * self.rozmiar_Kratki)) % self.szerokosc_Okna_Game), (glowa[1] + (y * self.rozmiar_Kratki)) % self.wysokosc_Okna_Game)
        # Jeśli nowa pozycja jest w miejscu ogona, Snake jest restowany
        if len(self.__pozycja) > 2 and nowa_Pozycja in self.__pozycja[2:]:
            self.reset()
            return False
        # Jeśli nowa pozycja będzie się równać krawędzi scian wąż zostanie zresetowany
        elif  ((nowa_Pozycja[1]) == 0 and y == 1) or ((nowa_Pozycja[1]) == self.wysokosc_Okna_Game - self.rozmiar_Kratki and y == -1):
            self.reset()
            return False
        elif ((nowa_Pozycja[0]) == 0 and x == 1) or ((nowa_Pozycja[0]) == self.szerokosc_Okna_Game - self.rozmiar_Kratki and x == -1):
            self.reset()
            return False
        else:
            # Przypisanie nowej pozycji do listy __pozycja
            self.__pozycja.append(nowa_Pozycja)
            # Usuwanie starej pozycji lub ominięcie kroku w wyniku snek się wydłuża
            if len(self.__pozycja) > self.__dlugosc:  del self.__pozycja[0]
            return True

    def reset(self):
        self.__dlugosc = 1
        self.__pozycja = [((self.szerokosc_Okna_Game / 2), (self.wysokosc_Okna_Game / 2))]
        self.__kierunek_ruchu = random.choice([self.gora, self.dol, self.lewo, self.prawo])
        self.punkty = 0

    def zdaj_raport(self):
        x, y = self.__kierunek_ruchu
        p=self.__pozycja[-1]
        pozycja = [p[0] , p[1]]

        wzrok=[2 * (p[0] + self.rozmiar_Kratki / 2 - self.szerokosc_Okna_Game / 2) / (self.szerokosc_Okna_Game + self.szerokosc_Kratki), 2 * (p[1] + self.rozmiar_Kratki / 2 - self.wysokosc_Okna_Game / 2) / (self.wysokosc_Okna_Game + self.szerokosc_Kratki)]


        return pozycja, wzrok,self.sprawdz_mozliwosci_ruchu()


    def sprawdz_mozliwosci_ruchu(self):
        glowa = self.pozycja_Glowy()
        x, y = self.__kierunek_ruchu
        # Nowa pozycja Snake na bazie pozycji jego głowy

        sensor_1=((glowa[0] + (x * self.rozmiar_Kratki)) % self.szerokosc_Okna_Game),(glowa[1] + (y * self.rozmiar_Kratki)) % self.wysokosc_Okna_Game

        sensor_1=glowa[0]+x*self.rozmiar_Kratki, glowa[1]+y*self.rozmiar_Kratki
        sensor_2=glowa[0]+y*self.rozmiar_Kratki, glowa[1]-x*self.rozmiar_Kratki
        sensor_3=glowa[0] - y * self.rozmiar_Kratki, glowa[1] + x * self.rozmiar_Kratki
        s1=s2=s3=0
        # Jeśli nowa pozycja będzie się równać krawędzi scian wąż zostanie zresetowany
        if ((sensor_1[0]) >= self.szerokosc_Okna_Game) or (sensor_1[0] <= 0 - self.rozmiar_Kratki):
            s1=1
        elif sensor_1[1] >= self.wysokosc_Okna_Game or sensor_1[1]<=0-self.rozmiar_Kratki:
            s1=1

        if ((sensor_2[0]) >= self.szerokosc_Okna_Game) or (sensor_2[0] <= 0 - self.rozmiar_Kratki):
            s2=1
        elif sensor_2[1] >= self.wysokosc_Okna_Game or sensor_2[1]<=0-self.rozmiar_Kratki:
            s2=1

        if ((sensor_3[0]) >= self.szerokosc_Okna_Game) or (sensor_3[0] <= 0 - self.rozmiar_Kratki):
            s3=1
        elif sensor_3[1] >= self.wysokosc_Okna_Game or sensor_3[1]<=0-self.rozmiar_Kratki:
            s3=1
        #print("Jestem tu i tu: ",glowa," sensor 1 jest tu: ", sensor_1)
       # print("Sprawdzam przedpole", s1, s2, s3)
        return s1,s2,s3



    def rysowanie(self, okno_Gry):
        # Odczytywanie listy od końca ponieważ nowa pozycja głowy jest na końcu listy
        # Dalsze współżędne na liście wskazują położenie części ogona węża
        for p in self.__pozycja[::-1]:
            if(p==self.__pozycja[-1]):
                r = pygame.Rect((p[0], p[1]), (self.rozmiar_Kratki, self.rozmiar_Kratki))
                x,y=self.__kierunek_ruchu

                sensor1 = pygame.Rect((p[0]+x*self.rozmiar_Kratki, p[1]+y*self.rozmiar_Kratki), (self.rozmiar_Kratki, self.rozmiar_Kratki))
                pygame.draw.rect(okno_Gry, self.kolor_1, sensor1)
                pygame.draw.rect(okno_Gry, (128, 128, 128), sensor1, 1)

                sensor2 = pygame.Rect((p[0]+y*self.rozmiar_Kratki, p[1]-x*self.rozmiar_Kratki), (self.rozmiar_Kratki, self.rozmiar_Kratki))
                pygame.draw.rect(okno_Gry, self.kolor_2, sensor2)
                pygame.draw.rect(okno_Gry, (128, 128, 128), sensor2, 1)

                sensor3 = pygame.Rect((p[0]-y*self.rozmiar_Kratki, p[1]+x*self.rozmiar_Kratki), (self.rozmiar_Kratki, self.rozmiar_Kratki))
                pygame.draw.rect(okno_Gry, self.kolor_3, sensor3)
                pygame.draw.rect(okno_Gry, (128, 128, 128), sensor3, 1)
                #Głowa
                pygame.draw.rect(okno_Gry, self.kolor_yellow, r)
                pygame.draw.rect(okno_Gry, (128, 128, 128), r, 1)

            else:

                r = pygame.Rect((p[0], p[1]), (self.rozmiar_Kratki, self.rozmiar_Kratki))
                pygame.draw.rect(okno_Gry, self.kolor, r)
                pygame.draw.rect(okno_Gry, (128, 128, 128), r, 1)
                #RYSOWANIE PUNKTOW SENSOROW

    def zjedzenie(self):
        self.__dlugosc += 1
        self.punkty += 1

    def kierunek_jedzenia(self,pozycja_jablka):
        glowa = self.pozycja_Glowy()
        x,y=pozycja_jablka
        return [x-glowa[0],y-glowa[1]]
