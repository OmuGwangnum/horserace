# coding: utf-8

from model import model
from data import Data

import numpy as np
import sys
import datetime

racekey = '07201811'
date = datetime.date(2020,3,29)
raceData = Data()
data, label = raceData.getRaceDataFromRaceKey(racekey, date)

print(data)

size = 18*5*13
model = model()
model.load('glass_short')
data = np.array(data)
data = np.reshape(data, (1, size))
print(data.shape)
pred = model.predict(data)
print(pred)
