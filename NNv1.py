
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

        model.fit(X, y, n_epoch=100, shuffle=True, run_id=self.filename)
        model.save(self.filename)
        return model

    def model(self,number_of_inputs,list_of_neurons):
        network = input_data(shape=[None, number_of_inputs-1, 1], name='input')
        for number_of_neurons in list_of_neurons:
            network = fully_connected(network, number_of_neurons, activation='relu')
        network = fully_connected(network, 1, activation='sigmoid')

        network = regression(network, optimizer='adam', learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(network, tensorboard_dir='log')
        return model



    def strip_data(self,training_data, number_of_sensors):

        data=[]
        for sample in training_data:
            sensors=[]
            for j in range(number_of_sensors):
                sensors.append(sample[j])
            sensors.append(sample[-3])
            sensors.append(sample[-2])
            sensors.append(sample[-1])
            data.append(sensors)
        return data


    def train(self):
        self.gra=Game(rozmiar_kratki=250)
        #training_data = self.gra.start(initial_games=2,sterowanie="ByHand",frame_rate=200,model_nn=None,number_of_sensors=None)
        training_data = self.gra.start(initial_games=500, sterowanie="Random", frame_rate=1, model_nn=None,
                                       number_of_sensors=None)
        #data_1=self.strip_data(training_data=training_data,number_of_sensors=3)

        nn_layout=[]
        nn_layout.append(500)
        nn_layout.append(100)
        #self.filname='nn1.tflearn'
        #nn_model = self.model(number_of_inputs=6,list_of_neurons=nn_layout)
        #nn_model = self.train_model(data_1, nn_model,number_of_inputs=6)

        self.filname = 'nn2.tflearn'
        data_2 = self.strip_data(training_data=training_data, number_of_sensors=7)
        nn_model2 = self.model(number_of_inputs=10, list_of_neurons=nn_layout)
        nn_model2 = self.train_model(data_2, nn_model2, number_of_inputs=10)

        nn_model2.load(self.filename)
        self.gra = Game(rozmiar_kratki=50)
        #self.gra.start(initial_games=1, sterowanie="AI", frame_rate=300, model_nn=nn_model,number_of_sensors=3)
        self.gra.start(initial_games=1, sterowanie="AI", frame_rate=300, model_nn=nn_model2, number_of_sensors=7)

ann1=NN1(initial_games=10, test_games=100, goal_steps=100, lr=1e-2, filename='nn1.tflearn')
ann1.train()
