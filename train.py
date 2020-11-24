# coding: utf-8

import pymysql.cursors
import numpy as np
import time
import sys

from data import Data
from model import model

data = Data()

x_train, y_train = data.getGlassShortTrainData()
x_train = np.array(x_train)
x_train = np.reshape(x_train, (x_train.shape[0], 900))
y_train = np.array(y_train)
x_test, y_test = data.getGlassShortTestData()
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], 900))
y_test = np.array(y_test)

model = model()
model.train(x_train, y_train)
model.save('glass_short')

model.eval(x_test, y_test)
