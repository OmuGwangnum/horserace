# coding: utf-8

from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.utils import np_utils

import os.path

class model:
    dim = 18*5*13
    model = None
    
    def __init__(self):
        model = Sequential()
        model.add(Dense(1200, activation='relu', input_dim=self.dim))
        model.add(Dropout(0.5))
        model.add(Dense(1200, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1200, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1200, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(18, activation='sigmoid'))
        model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        self.model = model

    def train(self, x_train, y_train):
        self.model.fit(x_train,
                       y_train,
                       verbose=1,
                       epochs=40)

    def train_generator(self, trains, valids):
        self.model.fit_generator(
            trains,
            validation_data=valids,
            epochs=40,
            shuffle=True
        )

    def eval(self, x_test, y_test):
        score = self.model.evaluate(x_test, y_test, verbose=1)
        return score

    def save(self, name):
        json_string = self.model.to_json()
        json_name = 'model/' + name + '.json'
        weight_name = 'model/' + name + '.hdf5'
        open(os.path.join('./', json_name), 'w').write(json_string)
        self.model.save_weights(os.path.join('./', weight_name))

    def load(self, name):
        json_name = 'model/' + name + '.json'
        weight_name = 'model/' + name + '.hdf5'
        json_string = open(os.path.join('./', json_name)).read()
        model = model_from_json(json_string)
        model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        model.load_weights(os.path.join('./', weight_name))
        self.model = model

    def predict(self, x):
        pred = self.model.predict(x, verbose=1)
        return pred
        
