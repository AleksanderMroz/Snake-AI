from Snake import Snake
from Apple import Apple

import pygame
import random
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter
import numpy as np


class Game:
    def __init__(self,rozmiar_kratki):
       pygame.init()
       self.szerokosc_Okna_Game = 1000
       self.wysokosc_Okna_Game = 1000
       self.szerokosc_Okna_Main = 1500
       self.wysokosc_Okna_Main = 1000
       self.czcionka = pygame.font.SysFont('comicsans', 30)
       # Zdefiniowanie wymiarów poszczegółnych kratek siatki
       self.rozmiar_Kratki = rozmiar_kratki
       self.szerokosc_Kratki = self.szerokosc_Okna_Game / self.rozmiar_Kratki
       self.wysokosc_Kratki = self.wysokosc_Okna_Game / self.rozmiar_Kratki
       self.played_games = 0
       self.done = False
       self.gora = (0, -1)
       self.dol = (0, 1)
       self.lewo = (-1, 0)
       self.prawo = (1, 0)
       self.vectors_and_keys = [
           [[0, -1], 0],
           [[0, 1], 1],
           [[-1, 0], 2],
           [[1, 0], 3]
       ]
       self.score = 0

       self.snake = Snake(self.szerokosc_Okna_Game,self.wysokosc_Okna_Game,self.rozmiar_Kratki,self.szerokosc_Kratki,self.wysokosc_Kratki)
       self.jablko = Apple(self.rozmiar_Kratki,self.szerokosc_Kratki,self.wysokosc_Kratki)
       self.history_of_game=[]


    def rysowanieSiatki(self,surface):
        # Linia pozioma
        surface.fill((0, 0, 0))
        for i in range(0, int(self.szerokosc_Kratki)):
            pygame.draw.line(surface, (128, 128, 128), (0, i * self.rozmiar_Kratki),
                             (self.szerokosc_Okna_Game, i * self.rozmiar_Kratki))
        # vertical lines
        for j in range(0, int(self.wysokosc_Kratki)):
            pygame.draw.line(surface, (128, 128, 128), (j * self.rozmiar_Kratki, 0),
                             (j * self.rozmiar_Kratki, self.wysokosc_Okna_Game))

    def steruj_recznie(self):
        run=True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Sterowanie do Snake'a
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.kierunek(self.gora)
                elif event.key == pygame.K_DOWN:
                    self.snake.kierunek(self.dol)
                elif event.key == pygame.K_LEFT:
                    self.snake.kierunek(self.lewo)
                elif event.key == pygame.K_RIGHT:
                    self.snake.kierunek(self.prawo)
        return run

    def steruj_randomowo(self):
        run=True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return run
            # Sterowanie do Snake'a
        action = random.randint(0, 3)
        #print("Wyegenrowano akcje", action)
        if action==0:
            self.snake.kierunek(self.gora)
        elif action==1:
            self.snake.kierunek(self.dol)
        elif action==2:
            self.snake.kierunek(self.lewo)
        elif action==3:
            self.snake.kierunek(self.prawo)

        return run

    def steruj_AI(self,model_NN,sensors,importance):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return run
        # Sterowanie do Snake'a
        x=[]

        for i in range(importance):
            x.append(sensors[i])

        predictions=[]
        for j in range(4):
            X = np.append(x,j).reshape(-1, importance + 1, 1)

            predictions.append(model_NN.predict(X))

        action = np.argmax(np.array(predictions))
        #print(sensors,action)
        print("Wyegenrowano akcje", action , predictions)
        if action == 0:
            self.snake.kierunek(self.gora)
        elif action == 1:
            self.snake.kierunek(self.prawo)
        elif action == 2:
            self.snake.kierunek(self.dol)
        elif action == 3:
            self.snake.kierunek(self.lewo)

        return run




    def start(self, initial_games, frame_rate, sterowanie,model_nn):

        # Inicjalizacja okna gry
        pygame.init()
        okno_Gry = pygame.display.set_mode((self.szerokosc_Okna_Main, self.wysokosc_Okna_Main), 0, 32)
        pygame.display.set_caption("SNAKE2")

        # Wyrasowanie siatki
        self.rysowanieSiatki(okno_Gry)
        # Inicjalizacja obiektów klas
        run = True
        step=1
        while (self.played_games < initial_games and run):
            pygame.time.delay(frame_rate)
            # Wyłączenie gry
            #print("\n\n\nNOWA AKCJA nr", step)
            glowa, wzrok, sensors = self.snake.zdaj_raport()
            s1, s2, s3 = sensors
            s6, s7 = self.snake.kierunek_jedzenia(self.jablko.pozycja)

            if sterowanie == "AI":
                run = self.steruj_AI(model_NN=model_nn,importance=5,sensors=[s1,s2,s3,glowa[0],glowa[1]])
            elif sterowanie == "ByHand":
                run = self.steruj_recznie()
            elif sterowanie == "Random":
                run =self.steruj_randomowo()
            still_alive=True
            # ODCZYTANIE WARTOŚCI SENSORÓW
            still_alive = self.snake.ruch()
            #print("Zrobiłem ruch o wartosci", self.snake.get_kierunek())
            step=step+1
            if (still_alive == False): self.played_games = self.played_games + 1
            #print("Jak się dla mnie skonczyl ruch", still_alive)

            if still_alive==True:
                nagroda=1
            else:
                nagroda=0
            self.history_of_game.append([s1,s2,s3,glowa[0],glowa[1],self.snake.get_kierunek(),nagroda])

            if self.snake.pozycja_Glowy() == self.jablko.pozycja:
                self.snake.zjedzenie()
                self.jablko.pozycja_Losowa()

            if still_alive == True:
                self.generuj_obraz(okno_Gry)
        else:
            print(self.history_of_game)
            return self.history_of_game

    def generuj_obraz(self, okno_Gry):
        glowa, wzrok, sensors = self.snake.zdaj_raport()
        s1, s2, s3 = sensors
        s6, s7 = self.snake.kierunek_jedzenia(self.jablko.pozycja)
        self.rysowanieSiatki(okno_Gry)
        self.snake.rysowanie(okno_Gry)
        self.jablko.rysuj(okno_Gry)
        okno_Gry.blit(okno_Gry, (0, 0))
        score = self.czcionka.render("Punkty: {0}".format(self.snake.punkty), 1, (255, 255, 0))
        sen0 = self.czcionka.render("Played games: {0}".format(self.played_games), 1, (255, 255, 0))
        sen1 = self.czcionka.render("Sensor 1: {0}".format(s1), 1, (255, 255, 0))
        sen2 = self.czcionka.render("Sensor 2: {0}".format(s2), 1, (255, 255, 0))
        sen3 = self.czcionka.render("Sensor 3: {0}".format(s3), 1, (255, 255, 0))
        sen4 = self.czcionka.render("Sensor 4: {0}".format(round(wzrok[0], 4)), 1, (255, 255, 0))
        sen5 = self.czcionka.render("Sensor 5: {0}".format(round(wzrok[1], 4)), 1, (255, 255, 0))
        sen6 = self.czcionka.render("Sensor 6: {0}".format(s6), 1, (255, 255, 0))
        sen7 = self.czcionka.render("Sensor 7: {0}".format(s7), 1, (255, 255, 0))
        # wzrok[0],wzrok[1],s6,s7
        okno_Gry.blit(sen0, (1055, 10))
        okno_Gry.blit(score, (1055, 40))
        okno_Gry.blit(sen1, (1055, 70))
        okno_Gry.blit(sen2, (1055, 100))
        okno_Gry.blit(sen3, (1055, 130))
        okno_Gry.blit(sen4, (1055, 160))
        okno_Gry.blit(sen5, (1055, 190))
        okno_Gry.blit(sen6, (1055, 220))
        okno_Gry.blit(sen7, (1055, 250))
        pygame.display.update()

        pass


def main():
    print("Jesteśmy tu")
    gra=Game(rozmiar_kratki=50)
    gra.start(initial_games=10,frame_rate=250,sterowanie="ByHand",model_nn=None)
    print("Koniec")

