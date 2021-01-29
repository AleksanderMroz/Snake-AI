
from random import randint
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

from Game import Game
class NN1:
    def __init__(self, initial_games=100, test_games=100, goal_steps=100, lr=1e-2, filename='nn1.tflearn'):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.filename = filename
        self.gra=None



    def train_model(self,training_data,model,number_of_inputs):
        X = []
        y = []
        for part in training_data:
            y.append([part[-1]])
            insert=[]
            for j in range(number_of_inputs-1):
                insert.append([part[j]])
            X.append(insert)

        model.fit(X, y, n_epoch=1, shuffle=True, run_id=self.filename)
        model.save(self.filename)
        return model

    def model(self,number_of_inputs):
        network = input_data(shape=[None, number_of_inputs-1, 1], name='input')
        network = fully_connected(network, 200, activation='relu')
        network = fully_connected(network, 30, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam', learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(network, tensorboard_dir='log')
        return model



    def train(self):
        self.gra=Game(rozmiar_kratki=250)
        training_data = self.gra.start(initial_games=500,sterowanie="Random",frame_rate=1,model_nn=None)
        nn_model = self.model(number_of_inputs=6)
        nn_model = self.train_model(training_data, nn_model,number_of_inputs=6)
        #nn_model.load(self.filename)
        self.gra = Game(rozmiar_kratki=250)
        self.gra.start(initial_games=1, sterowanie="AI", frame_rate=300, model_nn=nn_model)


ann1=NN1(initial_games=10, test_games=100, goal_steps=100, lr=1e-2, filename='nn1.tflearn')
ann1.train()
