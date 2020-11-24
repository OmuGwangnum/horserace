# coding: utf-8

import numpy as np
from data import Data
from model import model

data = Data()
x_test, y_test = data.getGlassShortTestData()

x_test = np.array(x_test)
print(x_test.shape)
x_test = np.reshape(len(x_test.shape[0]), 900)
y_test = np.array(y_test)

model = model()
model.load('glass_short')
model.eval(x_test, y_test)
