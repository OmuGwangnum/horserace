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

model = model()
model.load('glass_short')
data = np.array(data)
data = np.reshape(data, (1, 900))
print(data.shape)
pred = model.predict(data)
print(pred)
